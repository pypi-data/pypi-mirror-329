import numpy
from .lstsq import get_lstsq_solver
from .base import FeatureMapping
from ..detection.base import Features
from ...transformation import TransformationType
from ...transformation.scipy_backend import ScipyHomography

__all__ = ["ScipyLstSqFeatureMapping"]


class ScipyLstSqFeatureMapping(
    FeatureMapping, registry_id=FeatureMapping.RegistryId("LstSq", "Scipy")
):
    def __init__(self, transfo_type: TransformationType) -> None:
        self._solver = get_lstsq_solver(transfo_type)
        self._transfo_type = transfo_type
        super().__init__()

    def calculate(
        self, from_features: Features, to_features: Features
    ) -> ScipyHomography:
        passive = self._solver(to_features.coordinates, from_features.coordinates)
        return ScipyHomography(passive, self._transfo_type)

    def identity(self) -> ScipyHomography:
        return ScipyHomography(numpy.identity(3), TransformationType.identity)
