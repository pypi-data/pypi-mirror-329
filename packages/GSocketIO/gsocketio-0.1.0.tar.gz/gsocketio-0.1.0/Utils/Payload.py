import base64
import io
from json import dumps
from typing import Any, Dict, Iterator, Tuple, Union

import cv2 as cv
import numpy as np
from PIL import Image

from GSocketIO.Utils.Typing import ImageFmt


def is_base64(s: str) -> bool:
    try:
        base64.b64decode(s, validate=True)
        return True
    except:
        return False


def trans_i2b(
    image: Union[Image.Image, np.ndarray, str, Any], fmt: ImageFmt
) -> Union[str, Any]:
    encoded_str = image
    if isinstance(image, Image.Image):
        buffered = io.BytesIO()
        image.save(buffered, format=fmt.value["pil"])
        encoded_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    elif isinstance(image, np.ndarray):
        success, buffer = cv.imencode(fmt.value["cv"], image)
        if success:
            encoded_str = base64.b64encode(buffer).decode("utf-8")
    return encoded_str


def trans_b2i(
    b64_str: Union[str, Any], is_pil: bool
) -> Union[Image.Image, np.ndarray, Any]:
    image = b64_str
    if is_base64(b64_str):
        if is_pil:
            decoded_bytes = base64.b64decode(b64_str)
            buffered = io.BytesIO(decoded_bytes)
            image = Image.open(buffered)
        else:
            decoded_bytes = base64.b64decode(b64_str)
            matrix = np.frombuffer(decoded_bytes, dtype=np.uint8)
            image = cv.imdecode(matrix, cv.IMREAD_COLOR)
    return image


class OnData:
    def __init__(self, data: Dict[str, Any], is_pil: bool = True) -> None:
        for k, v in data.items():
            v = trans_b2i(v, is_pil)
            setattr(self, k, v)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for k, v in self.__dict__.items():
            yield k, v


class EmitData:
    def __init__(self, data: Dict[str, Any], fmt: ImageFmt = ImageFmt.Jpg) -> None:
        for k, v in data.items():
            v = trans_i2b(v, fmt=fmt)
            setattr(self, k, v)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for k, v in self.__dict__.items():
            yield k, v

    @property
    def json(self) -> str:
        return dumps(self.__dict__)
