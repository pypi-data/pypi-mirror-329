from __future__ import annotations
import logging
import abc
from typing import Dict
from enum import Enum
import io
import time
from dataclasses import dataclass
from typing import List, Optional, Type
import uuid
import msgpack
from PIL import Image

from moth.message.exceptions import FailedToParseMessage, UnknownMessageType

logger = logging.getLogger(__name__)

class HandshakeTaskTypes(str, Enum):
    CLASSIFICATION = "classification"
    OBJECT_DETECTION = "object_detection"
    SEGMENTATION = "segmentation"


def parse_message(msg: bytes) -> Msg:
    try:
        envelope = msgpack.unpackb(msg)
        message_type = envelope["msgType"]

        if message_type not in _MESSAGE_CLASSES:
            raise UnknownMessageType(f"Cannot parse message of type: {message_type}")

        message_class = _MESSAGE_CLASSES[message_type]
        return message_class.deserialize(envelope["payload"])

    except msgpack.exceptions.ExtraData as e:
        logger.error("msgpack.exceptions.ExtraData")
        logger.exception(e)
        raise FailedToParseMessage(f"Invalid message format: {e}")


class Msg(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError()

    @classmethod
    def msg_type_name(cls):
        return cls.__name__

    def serialize_envelope(self) -> bytes:
        """
        Serialize the message and wrap it in an envelope so the recipient can check the
        message type and route the payload to the appropriate message parser.
        Use the `parse_message` function to unpack the message.
        """
        payload = self.serialize()
        envelope = {"msgType": self.msg_type_name(), "payload": payload}
        return msgpack.packb(envelope)

    @staticmethod
    def deserialize(data: bytes) -> Msg:
        raise NotImplementedError()


class HeartbeatMsg(Msg):
    def __init__(self, timestamp: Optional[int] = None):
        if timestamp == None:
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp

    def serialize(self):
        obj = {
            "t": self.timestamp,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(data: bytes) -> HeartbeatMsg:
        obj = msgpack.unpackb(data)
        return HeartbeatMsg(obj["t"])


class ImagePromptMsg(Msg):
    def __init__(self, image: Image.Image, id: Optional[str] = None):
        self.image = image
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def serialize(self):
        # Convert the image to bytes
        with io.BytesIO() as output:
            self.image.save(output, format="PNG")
            img_bytes = output.getvalue()

        obj = {
            "id": self.id,
            "imageBytes": img_bytes,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(bytes) -> ImagePromptMsg:
        obj = msgpack.unpackb(bytes)
        id = obj.get("id")
        img = Image.open(io.BytesIO(obj["imageBytes"]))
        return ImagePromptMsg(img, id)


@dataclass
class ClassificationResultMsg(Msg):
    prompt_id: str
    class_index: Optional[int] = None
    class_name: Optional[str] = None
    confidence: Optional[float] = None

    def serialize(self):
        obj = {
            "promptId": self.prompt_id,
            "classIndex": self.class_index,
            "className": self.class_name,
            "confidence": self.confidence,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(bytes) -> ClassificationResultMsg:
        obj = msgpack.unpackb(bytes)
        return ClassificationResultMsg(
            prompt_id=obj["promptId"],
            class_index=obj.get("classIndex"),
            class_name=obj.get("className"),
            confidence=obj.get("confidence", None),
        )


class ObjectDetectionResult:
    """
    COCO-style bounding box annotation.
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        class_index: Optional[int] = None,
        class_name: Optional[str] = None,
        confidence: Optional[float] = None,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.class_index = class_index
        self.class_name = class_name
        self.confidence = confidence

    def serialize(self):
        obj = {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "classIndex": self.class_index,
            "className": self.class_name,
            "confidence": self.confidence,
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(bytes) -> ObjectDetectionResult:
        obj = msgpack.unpackb(bytes)
        return ObjectDetectionResult(
            x=obj["x"],
            y=obj["y"],
            w=obj["w"],
            h=obj["h"],
            class_index=obj.get("classIndex"),
            class_name=obj.get("className"),
            confidence=obj.get("confidence"),
        )


class ObjectDetectionResultMsg(Msg):
    """
    Message for object detection results.
    A list of bounding boxes.
    """

    def __init__(
        self, prompt_id: str, object_detection_results: List[ObjectDetectionResult]
    ):
        self.prompt_id = prompt_id
        self.object_detection_results = object_detection_results

    def serialize(self):
        obj = {
            "promptId": self.prompt_id,
            "results": [bb.serialize() for bb in self.object_detection_results],
        }

        return msgpack.packb(obj)

    @staticmethod
    def deserialize(bytes) -> ObjectDetectionResultMsg:
        obj = msgpack.unpackb(bytes)
        return ObjectDetectionResultMsg(
            prompt_id=obj["promptId"],
            object_detection_results=[
                ObjectDetectionResult.deserialize(bb) for bb in obj["results"]
            ],
        )


class SegmentationResult:
    """
    Segmentation in the format of [x1, y1, x2, y2, ...].
    """

    def __init__(
        self,
        points: List[int],
        class_index: Optional[int] = None,
        class_name: Optional[str] = None,
        confidence: float = None,
    ) -> None:
        self.points = points
        self.class_name = class_name
        self.class_index = class_index
        self.confidence = confidence

    def serialize(self) -> bytes:
        obj = {
            "points": self.points,
            "className": self.class_name,
            "classIndex": self.class_index,
            "confidence": self.confidence,
        }
        return msgpack.packb(obj)

    @staticmethod
    def deserialize(data: bytes) -> Msg:
        obj = msgpack.unpackb(data)
        return SegmentationResult(
            points=obj["points"],
            class_name=obj["className"],
            class_index=obj["classIndex"],
            confidence=obj["confidence"],
        )


class SegmentationResultMsg(Msg):
    """
    Message for segmentation results.
    List of SegmentationResults.
    """

    def __init__(self, prompt_id: str, results: List[SegmentationResult]):
        self.prompt_id = prompt_id
        self.results = results

    def serialize(self) -> bytes:
        obj = {
            "promptId": self.prompt_id,
            "results": [r.serialize() for r in self.results],
        }
        return msgpack.packb(obj)

    @staticmethod
    def deserialize(data: bytes) -> Msg:
        obj = msgpack.unpackb(data)
        return SegmentationResultMsg(
            prompt_id=obj["promptId"],
            results=[SegmentationResult.deserialize(r) for r in obj["results"]],
        )


@dataclass
class HandshakeMsg(Msg):
    name: str
    handshake_token: str
    version: str = "v0"
    task_type: HandshakeTaskTypes = HandshakeTaskTypes.CLASSIFICATION
    output_classes: Optional[List[str]] = None

    def serialize(self) -> bytes:
        obj = {
            "name": self.name,
            "token": self.handshake_token,
            "version": self.version,
            "taskType": self.task_type,
            "outputClasses": self.output_classes,
        }
        return msgpack.packb(obj)

    @staticmethod
    def deserialize(data: bytes) -> HandshakeMsg:
        obj = msgpack.unpackb(data)
        return HandshakeMsg(
            name=obj["name"],
            handshake_token=obj["token"],
            version=obj["version"],
            task_type=obj.get(
                "taskType", HandshakeTaskTypes.CLASSIFICATION
            ),  # Ensure backwards compatibility
            output_classes=obj.get(
                "outputClasses", None
            ),  # Ensure backwards compatibility
        )


@dataclass
class HandshakeResponseMsg(Msg):
    def serialize(self) -> bytes:
        return msgpack.packb({})

    @staticmethod
    def deserialize(data: bytes) -> HandshakeResponseMsg:
        return HandshakeResponseMsg()


class PromptResultMsg(Msg):
    pass


_MESSAGE_CLASSES: Dict[str, Type[Msg]] = {
    HandshakeMsg.msg_type_name(): HandshakeMsg,
    HandshakeResponseMsg.msg_type_name(): HandshakeResponseMsg,
    HeartbeatMsg.msg_type_name(): HeartbeatMsg,
    ImagePromptMsg.msg_type_name(): ImagePromptMsg,
    PromptResultMsg.msg_type_name(): ClassificationResultMsg,  # Ensure backwards compatibility
    ClassificationResultMsg.msg_type_name(): ClassificationResultMsg,
    ObjectDetectionResultMsg.msg_type_name(): ObjectDetectionResultMsg,
    SegmentationResultMsg.msg_type_name(): SegmentationResultMsg
}
