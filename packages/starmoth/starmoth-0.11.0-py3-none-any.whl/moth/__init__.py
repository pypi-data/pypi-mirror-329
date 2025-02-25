import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import zmq
import time
from typing import Optional, List

import zmq.asyncio

from moth.log import configure_moth_logger
from moth.message import (
    HandshakeMsg,
    HandshakeResponseMsg,
    HeartbeatMsg,
    ImagePromptMsg,
    Msg,
    parse_message,
    HandshakeTaskTypes,
)
from moth.message.exceptions import MothMessageError

HEARTBEAT_TIMEOUT = 5
HEARTBEAT_INTERVAL = 1

configure_moth_logger()
logger = logging.getLogger(__name__)
class Moth:
    def __init__(
        self,
        name: str,
        token: str = "",
        task_type: HandshakeTaskTypes = HandshakeTaskTypes.CLASSIFICATION,
        output_classes: Optional[List[str]] = None,
        max_workers = 4
    ):
        self.name = name
        self._token = token
        self.stop = False
        self.task_type = task_type
        self.output_classes = output_classes
        self.stop_event = asyncio.Event()
        self._PROMPT_FUNCTIONS = []
        self.max_workers = max_workers

    def prompt(self, func):
        self._PROMPT_FUNCTIONS.append(func)
        return func

    async def heartbeat_loop(self):
        """Sends heartbeat messages periodically."""
        while True:
            await asyncio.sleep(HEARTBEAT_INTERVAL)  # Send heartbeat at an interval
            await self.socket.send(HeartbeatMsg().serialize_envelope())

    async def message_loop(self, executor):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)
        last_heartbeat = None

        handshake = HandshakeMsg(
            self.name, self._token, "v0.0.0", self.task_type, self.output_classes
        )
        await self.socket.send(handshake.serialize_envelope())

        logger.info("MoTH client is running")
        while not self.stop_event.is_set():
            events = await self.socket.poll(1000)  # Use asyncio poll for non-blocking

            if events:
                msg_bytes = await self.socket.recv()
                last_heartbeat = time.time() # any message from the server counts as a heartbeat

                # Process the message in a thread pool
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(executor, self.process_message, msg_bytes)

                if response is not None and isinstance(response, Msg):
                    await self.socket.send(response.serialize_envelope())

            if (last_heartbeat is not None and time.time() - last_heartbeat > HEARTBEAT_TIMEOUT):
                logger.debug(f"Time since heartbeat: {time.time() - last_heartbeat}")
                logger.info("Lost connection to server")
                self.stop_event.set()

        for task in asyncio.all_tasks():
            task.cancel()
            

    def process_message(self, msg_bytes):
        """Blocking function to process messages."""
        message = parse_message(msg_bytes)

        if isinstance(message, ImagePromptMsg):
            func = self._PROMPT_FUNCTIONS[0]
            return func(message)

        if isinstance(message, HeartbeatMsg):
            logger.debug(f"Got heartbeat from server")

        if isinstance(message, HandshakeResponseMsg):
            logger.info("Connected to server")
        
        logger.debug(f"Processed: {message}")

    def run(self, url="tcp://localhost:7171"):
        context = zmq.asyncio.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, self.name)

        self.socket.connect(url)

        try:
            asyncio.run(self.run_task())
        except KeyboardInterrupt:
            logger.info("Received KeyboardInterrupt, exiting...")
        except asyncio.exceptions.CancelledError:
            context.destroy()
            logger.info("Shutdown")

    async def run_task(self):
        executor = ThreadPoolExecutor(max_workers=self.max_workers)
        # Start message handling and heartbeat as concurrent tasks
        tasks = [
            asyncio.create_task(self.message_loop(executor)),
            asyncio.create_task(self.heartbeat_loop())
        ]

        await asyncio.gather(*tasks)

def main():
    print(
        """
    ███╗░░░███╗░█████╗░████████╗██╗░░██╗
    ████╗░████║██╔══██╗╚══██╔══╝██║░░██║
    ██╔████╔██║██║░░██║░░░██║░░░███████║
    ██║╚██╔╝██║██║░░██║░░░██║░░░██╔══██║
    ██║░╚═╝░██║╚█████╔╝░░░██║░░░██║░░██║
    ╚═╝░░░░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝
    """
    )
