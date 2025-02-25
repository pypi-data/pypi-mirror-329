from typing import Optional
import numpy
from ...registry import Registered
from ..features import Features

__all__ = ["FeatureDetector"]


class FeatureDetector(Registered, register=False):
    def __init__(self, mask: Optional[numpy.ndarray] = None) -> None:
        self._mask = mask

    def find(self, arr: numpy.ndarray) -> Features:
        raise NotImplementedError
