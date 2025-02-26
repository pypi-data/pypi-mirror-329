import numpy as np
from qwen_vl_utils import smart_resize


def detections_to_suffix_formatter(
    xyxy: np.ndarray,
    class_id: np.ndarray,
    classes: list[str],
    resolution_wh: tuple[int, int],
    min_pixels: int,
    max_pixels: int,
) -> str:
    image_w, image_h = resolution_wh
    input_h, input_w = smart_resize(height=image_h, width=image_w, min_pixels=min_pixels, max_pixels=max_pixels)

    xyxy = xyxy / [image_w, image_h, image_w, image_h]
    xyxy = xyxy * [input_w, input_h, input_w, input_h]
    xyxy = xyxy.astype(int)

    detection_lines = []
    for cid, box in zip(class_id, xyxy):
        label = classes[int(cid)]
        bbox_str = ", ".join(str(num) for num in box.tolist())
        line = f'\t{{"bbox_2d": [{bbox_str}], "label": "{label}"}}'
        detection_lines.append(line)

    joined_detections = ",\n".join(detection_lines)
    formatted_str = f"```json\n[\n{joined_detections}\n]\n```"
    return formatted_str


def detections_to_prefix_formatter(
    xyxy: np.ndarray, class_id: np.ndarray, classes: list[str], resolution_wh: tuple[int, int]
) -> str:
    return "Outline the position of " + ", ".join(classes) + ". Output all the coordinates in JSON format."
