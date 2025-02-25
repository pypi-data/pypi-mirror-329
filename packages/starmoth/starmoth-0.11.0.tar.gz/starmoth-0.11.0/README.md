
# MOdel Test Harness (Moth)

A simple way to interrogate your AI model from a separate testing application.

# Client

## Simple classification model client.
``` python
from moth import Moth
from moth.message import ImagePromptMsg, ClassificationResultMsg, HandshakeTaskTypes

moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION)

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    return ClassificationResultMsg(prompt_id=prompt.id, class_name="cat") # Most pictures are cat pictures 

moth.run()
```

ClassificationResultMsg can optionally include a confidence value

``` python
ClassificationResultMsg(prompt_id=prompt.id, class_name="cat", confidence=0.9)
```

## Simple object detection model client.
``` python
from moth import Moth
from moth.message import (
    ImagePromptMsg,
    ObjectDetectionResultMsg,
    ObjectDetectionResult,
    HandshakeTaskTypes,
)

moth = Moth("my-ai", task_type=HandshakeTaskTypes.OBJECT_DETECTION)


@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    # Make a list of ObjectDetectionResults
    results = []
    results.append(
        ObjectDetectionResult(
            0,
            0,
            50,
            50,
            class_name="cat",
            class_index=0,
            confidence=0.9,  # Optional confidence
        )
    )
    results.append(
        ObjectDetectionResult(
            10,
            10,
            50,
            35,
            class_name="dog",
            class_index=1,
            confidence=0.1,  # Optional confidence
        )
    )
    return ObjectDetectionResultMsg(
        prompt_id=prompt.id, object_detection_results=results
    )


moth.run()

```

## Simple segmentation model client.
``` python
from moth import Moth
from moth.message import (
    ImagePromptMsg,
    SegmentationResultMsg,
    SegmentationResult,
    HandshakeTaskTypes,
)

moth = Moth("my-ai", task_type=HandshakeTaskTypes.SEGMENTATION)


@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    # Make a list of ObjectDetectionResults
    results = []
    results.append(
        SegmentationResult(
            [0, 0, 50, 50, 20, 20, 0, 0],  # The predicted polygon
            class_name="cat",
            class_index=0,
            confidence=0.9,  # Optional confidence
        )
    )
    results.append(
        SegmentationResult(
            [0, 0, 50, 50, 13, 20, 0, 0],  # The predicted polygon
            class_name="dog",
            class_index=1,
            confidence=0.1,  # Optional confidence
        )
    )
    return SegmentationResultMsg(prompt_id=prompt.id, results=results)


moth.run()
```

## Mask to polygon conversion
Easily convert a binary mask to a polygon using the convert_mask_to_contour function from the `moth.utils` module.

### Usage
1. Import the function:
    ``` python
    from moth.utils import convert_mask_to_contour
    ```
2. Prepare Your Mask: Ensure your mask is a 2D NumPy array where regions of interest are marked with 1s (or 255 for 8-bit images) and the background is 0.
3. Convert the mask:
    ``` python
    polygon = convert_mask_to_contour(mask)
    ```
### Example
``` python
from moth.utils import convert_mask_to_contour
import numpy as np

# Example binary mask
mask = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
], dtype=np.uint8)

# Convert the mask to a polygon
polygon = convert_mask_to_contour(mask)

# Output the polygon
print(polygon)
```

## Client Output Classes
Define the set of output classes that your model can predict. This information is sent to the server so it knows the possible prediction classes of the model. This is recommended to ensure the model is not penalized for classes it cannot output:
``` python
moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION, output_classes=["cat", "dog"])
```
By specifying these output classes, the server can accurately assess the model's performance based on its intended capabilities, preventing incorrect evaluation against classes it is not designed to predict.


# Server

## Simple server.
``` python
from moth.server import Server
from moth.message import HandshakeMsg

class ModelDriverImpl(ModelDriver):
    # TODO: Implement your model driver here
    pass

server = Server(7171)

@server.driver_factory
def handle_handshake(handshake: HandshakeMsg) -> ModelDriver
    return ModelDriverImpl()

server.start()
```
## Subscribe to model changes
Track changes to the list of connected models:
``` python
from moth.server import Model

@server.on_model_change
def handle_model_change(model_list: List[Model]):
    print(f"Connected models: {model_list}")
```
