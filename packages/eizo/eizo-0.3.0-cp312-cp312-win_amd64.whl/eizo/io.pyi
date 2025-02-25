from pathlib import Path
from enum import Enum
import numpy as np
from typing import Union


class ColorMode(Enum):
    Auto = 0
    RGB = 1
    Gray = 2


def read(
        path: Union[str | Path], color_mode: ColorMode = ColorMode.Auto
) -> np.ndarray: ...


def write(path: Union[str | Path], img: np.ndarray): ...


__all__ = [
    "read",
    "write",
    "ColorMode",
]
