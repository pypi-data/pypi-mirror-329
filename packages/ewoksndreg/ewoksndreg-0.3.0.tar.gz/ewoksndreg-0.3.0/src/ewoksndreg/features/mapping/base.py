from ..detection.base import Features
from ...transformation.base import Transformation
from ...registry import Registered


__all__ = ["FeatureMapping"]


class FeatureMapping(Registered, register=False):
    def identity(self) -> Transformation:
        raise NotImplementedError

    def calculate(
        self, from_features: Features, to_features: Features
    ) -> Transformation:
        raise NotImplementedError
