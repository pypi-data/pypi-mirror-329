from typing import Type, Sequence, Optional
import numpy
from .types import TransformationType
from ..registry import Registered

__all__ = ["Transformation"]


class Transformation(Registered, register=False):
    def __init__(self, transfo_type: TransformationType) -> None:
        if isinstance(transfo_type, str):
            transfo_type = TransformationType(transfo_type)
        self._type = transfo_type

    @property
    def type(self) -> TransformationType:
        return self._type

    def as_type(self, cls: Type["Transformation"]) -> "Transformation":
        if isinstance(self, cls):
            return self
        raise TypeError(f"cannot convert '{type(self).__name__}' to '{cls.__name__}'")

    def is_homography(self):
        return self._type in [
            "identity",
            "translation",
            "rigid",
            "similarity",
            "affine",
            "projective",
        ]

    def apply_coordinates(self, coord: Sequence[numpy.ndarray]) -> numpy.ndarray:
        """
        :param coord: shape `(N, M)`
        :returns: shape `(N, M)`
        """
        raise NotImplementedError

    def apply_data(
        self,
        data: numpy.ndarray,
        offset: Optional[numpy.ndarray] = None,
        shape: Optional[numpy.ndarray] = None,
        cval=numpy.nan,
        interpolation_order: int = 1,
    ) -> numpy.ndarray:
        """
        :param data: shape `(N1, N2, ..., M1, M2, ...)` with `len((N1, N2, ...)) = N`
        :param offset: shape `(N,)`
        :param shape: shape `(N,) = [N1', N2', ...]`
        :param cval: missing value
        :param interpolation_order: order of interpolation: 0 is nearest neighbor, 1 is bilinear,...
        :returns: shape `(N1', N2', ..., M1, M2, ...)`
        """
        raise NotImplementedError

    def __mul__(self, other: "Transformation") -> "Transformation":
        """When appyling the transformation, `other` comes after `self`"""
        raise NotImplementedError
