import abc
from PIL import Image, ImageOps
from pathlib import Path
from typing import Optional, Union

from moth.message import ImagePromptMsg, ClassificationResultMsg, ObjectDetectionResultMsg


class ModelDriver(abc.ABC):
    @abc.abstractmethod
    def on_model_result(self, result: Union[ClassificationResultMsg, ObjectDetectionResultMsg]):
        raise NotImplementedError()

    @abc.abstractmethod
    def next_model_prompt(self) -> Optional[ImagePromptMsg]:
        raise NotImplementedError()

class NoOpDriver(ModelDriver):
    def on_model_result(self, result: ClassificationResultMsg):
        pass
    
    def next_model_prompt(self) -> Optional[ImagePromptMsg]:
        return None

class TestImagesInFolder(ModelDriver):
    def __init__(self, folder, ext="png"):
        self.folder = folder
        self.files = Path(folder).glob(f"*.{ext}")
        self._rubric = {}
        self._correct_count = 0
        self._error_count = 0

    def on_model_result(self, result: ClassificationResultMsg):
        if result.prompt_id not in self._rubric:
            print("What question are you answering?")
            return

        expected_answer = self._rubric[result.prompt_id]
        if expected_answer == result.class_name:
            self._correct_count += 1
            print(f"Correct! {self._score_card()}")
        else:
            self._error_count += 1
            print(f"Error :( {self._score_card()}")

    def next_model_prompt(self) -> Optional[ImagePromptMsg]:
        try:
            next_file = next(self.files)
            name = next_file.name
            expected_answer = name.split("_")[0]

            image = Image.open(next_file)

            if image.mode == "RGBA":
                background = Image.new("RGBA", image.size, (255, 255, 255))
                image = ImageOps.invert(
                    Image.alpha_composite(background, image).convert("RGB")
                )

            propmpt = ImagePromptMsg(image)
            self._rubric[propmpt.id] = expected_answer
            return propmpt
        except StopIteration:
            # No more files in the folder
            return None

    def _score_card(self) -> str:
        correct = self._correct_count
        total = self._correct_count + self._error_count
        return f"({correct}/{total})"
