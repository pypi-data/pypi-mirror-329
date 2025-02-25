""" Server module for the Moth project. """

import logging
import asyncio
import signal
import threading
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
import time
import zmq
import zmq.asyncio
from moth.driver import ModelDriver
from moth.message import (
    HandshakeMsg,
    HandshakeResponseMsg,
    HeartbeatMsg,
    ClassificationResultMsg,
    ObjectDetectionResultMsg,
    SegmentationResultMsg,
    parse_message,
)

logger = logging.getLogger(__name__)

HEARTBEAT_TIMEOUT = 5
HEARTBEAT_INTERVAL = 1


@dataclass
class Model:
    """Holds information about a model that is connected to the server."""

    id: str
    task_type: str
    output_classes: Optional[List[str]] = None

    def serialize(self):
        return {
            "id": self.id,
            "taskType": self.task_type,
            "outputClasses": self.output_classes,
        }

    @staticmethod
    def deserialize(json) -> "Model":
        return Model(
            id=json["id"],
            task_type=json["taskType"],
            output_classes=json["outputClasses"],
        )


class ClientConnection:
    def __init__(
        self,
        client_id: str,
        driver: ModelDriver,
        model: Model,
        heartbeat: asyncio.Task,
        prompt_worker: asyncio.Task,
    ):
        self.client_id = client_id
        self.driver = driver
        self.model = model
        self.heartbeat = heartbeat
        self.prompt_worker = prompt_worker
        self.last_heartbeat = time.time()

    @property
    def identity(self) -> str:
        return self.client_id.encode("utf-8")

    def mark_heartbeat_timestamp(self, t: Optional[float] = None):
        if t is None:
            self.last_heartbeat = time.time()
        else:
            self.last_heartbeat = t

    def is_timeout(self) -> bool:
        return time.time() - self.last_heartbeat > HEARTBEAT_TIMEOUT

    async def on_disconnect(self):
        self.heartbeat.cancel()
        self.prompt_worker.cancel()
        await self.heartbeat
        await self.prompt_worker


class Server:
    """Server class that accepts connections from models."""

    def __init__(self, port: int = 7171):
        self.port = port
        self._stop = False
        self._driver_factory: Optional[Callable[[HandshakeMsg], ModelDriver]] = None
        self._clients: Dict[bytes, ClientConnection] = {}
        self._client_list_callback: Optional[Callable[[List[Model]], None]] = None
        self.prompt_queue = asyncio.Queue()
        self.stop_event = asyncio.Event()

    def start(self):
        try:
            asyncio.run(self._start_event_loop())
        except Exception as err:
            logger.error("Something bad happened")
            logger.exception(err)

    def stop(self):
        logger.info(f"Server is stopping")
        self.stop_event.set()

    def driver_factory(self, func: Callable[[HandshakeMsg], ModelDriver]):
        """
        Annotation to provide driver factory function.
        For every incoming model connection, this factory is called to get a driver for
        that model.
        """
        self._driver_factory = func
        return func

    def on_model_change(self, func: Callable[[List[Model]], None]):
        """
        Annotation to provide a function that is called when the list of connected models changes.
        """
        self._client_list_callback = func
        return func

    async def _start_event_loop(self):
        self.stop_event = asyncio.Event()
        self.prompt_queue = asyncio.Queue()
        self.context = zmq.asyncio.Context()

        loop = asyncio.get_running_loop()
        if threading.current_thread() is threading.main_thread():
            # Signals can only be changed on main thread
            loop.add_signal_handler(
                signal.SIGINT, lambda: asyncio.create_task(self._shutdown(signal.SIGINT))
            )
            loop.add_signal_handler(
                signal.SIGTERM, lambda: asyncio.create_task(self._shutdown(signal.SIGTERM))
            )

        socket = self.context.socket(zmq.ROUTER)
        socket.bind(f"tcp://*:{self.port}")
        asyncio.create_task(self._process_prompt_queue(socket))
        await self._recv_loop(socket)

    async def _shutdown(self, signal):
        logger.info(f"Received exit signal {signal.name}")
        self.stop_event.set()

    async def _send_heartbeat(self, socket, identity):
        logger.debug(f"Start heartbeat for {identity.decode('utf-8')}")
        try:
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                logger.debug(f"Sending heartbeat to {identity.decode('utf-8')}")
                await socket.send_multipart(
                    [identity, HeartbeatMsg().serialize_envelope()]
                )
        except asyncio.exceptions.CancelledError:
            logger.debug(f"Stop heartbeat for {identity.decode('utf-8')}")

    async def _process_prompt_queue(self, socket):
        logger.debug(f"Start processing prompt queue")
        try:
            while True:
                # The prompt queue contains messages that are ready to send: Tuple[bytes, bytes]
                # The first bytes is the identity, second is the message payload
                prompt_msg = await self.prompt_queue.get()
                logger.debug(f"Sending prompt to {prompt_msg[0].decode('utf-8')}")
                await socket.send_multipart(prompt_msg)
        except asyncio.exceptions.CancelledError:
            logger.debug(f"Stop processing prompt queue")

    def _prepare_prompt_message(
        self, driver: ModelDriver, identity
    ) -> Optional[tuple[bytes, bytes]]:
        prompt = driver.next_model_prompt()
        if prompt is None:
            return None

        return (identity, prompt.serialize_envelope())

    async def _prompt_worker(self, identity, driver):
        logger.debug(f"Start prompt_worker for {identity.decode('utf-8')}")
        try:
            while True:
                try:
                    # Loading a test case and serializing the image may take a second or more
                    # Do that work on a thread and queue the result when its done
                    prompt_msg = await asyncio.to_thread(
                        self._prepare_prompt_message, driver, identity
                    )
                    if prompt_msg is not None:
                        logger.debug(f"Queue prompt for {identity.decode('utf-8')}")
                        await self.prompt_queue.put(prompt_msg)
                    else:
                        await asyncio.sleep(1)  # Small sleep to avoid busy looping
                except Exception as e:
                    logger.error(f"Error generating prompt for {identity}: {e}")
        except asyncio.exceptions.CancelledError:
            logger.debug(f"Stop prompts for {identity.decode('utf-8')}")

    def _create_new_client_connection(self, identity, socket, message: HandshakeMsg):
        client_driver = self._driver_factory(message)
        prompt_task = asyncio.create_task(self._prompt_worker(identity, client_driver))
        heartbeat_task = asyncio.create_task(self._send_heartbeat(socket, identity))

        model = Model(
            id=identity.decode("utf-8"),
            task_type=message.task_type,
            output_classes=message.output_classes,
        )
        new_client = ClientConnection(
            identity.decode("utf-8"), client_driver, model, heartbeat_task, prompt_task
        )
        return new_client

    async def _recv_loop(self, socket):
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)

        logger.info("Server listening...")
        while not self.stop_event.is_set():
            events = await socket.poll(1000)  # Use asyncio poll for non-blocking

            if events:
                identity, msg_bytes = await socket.recv_multipart()
                client = None
                if identity in self._clients:
                    client = self._clients[identity]

                try:
                    message = parse_message(msg_bytes)
                    if isinstance(message, HandshakeMsg) and self._driver_factory:
                        new_client = self._create_new_client_connection(
                            identity, socket, message
                        )
                        self._clients[identity] = new_client
                        if self._client_list_callback:
                            self._client_list_callback([client.model for _, client in self._clients.items()])
                        logger.info(f"Client connected: {new_client.client_id}")
                        await socket.send_multipart(
                            [identity, HandshakeResponseMsg().serialize_envelope()]
                        )
                    elif isinstance(
                        message,
                        (
                            ClassificationResultMsg,
                            ObjectDetectionResultMsg,
                            SegmentationResultMsg,
                        ),
                    ):
                        if client is not None:
                            # Can this happen? Why do we get a result from a client that is not connected
                            client.driver.on_model_result(message)

                    # Any message counts as a heartbeat
                    if client is not None:
                        client.mark_heartbeat_timestamp()

                except Exception as e:
                    logger.error(f"Unhandled exception: {e}")
                    logger.exception(e)

            # Handle heartbeats and check for disconnections
            disconnected = [
                identity
                for identity, client in self._clients.items()
                if client.is_timeout()
            ]
            for identity in disconnected:
                disconnected_client = self._clients[identity]
                await disconnected_client.on_disconnect()
                self._clients.pop(identity)
                logger.info(f"Client disconnected: {disconnected_client.client_id}")
            if len(disconnected) > 0 and self._client_list_callback is not None:
                self._client_list_callback(
                    [client.model for _, client in self._clients.items()]
                )

        # Clean up resources
        logger.info("Shutting down server...")
        socket.close()
        self.context.term()
