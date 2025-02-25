from typing import Optional, Dict, Callable, Sequence
import numpy
from skimage.measure import ransac

from .base import FeatureMapping
from ..detection.base import Features
from ...transformation import TransformationType
from ...transformation.numpy_backend import NumpyHomography
from ...transformation.scikitimage_backend import ShiftTransform
from ...transformation.scikitimage_backend import EuclideanTransform
from ...transformation.scikitimage_backend import SimilarityTransform
from ...transformation.scikitimage_backend import AffineTransform
from ...transformation.scikitimage_backend import ProjectiveTransform

__all__ = ["SciKitImageRansacFeatureMapping"]


class SciKitImageRansacFeatureMapping(
    FeatureMapping, registry_id=FeatureMapping.RegistryId("Ransac", "SciKitImage")
):
    def __init__(
        self, transfo_type: TransformationType, solve_options: Optional[Dict] = None
    ) -> None:
        if solve_options is None:
            solve_options = dict()
        solve_options.setdefault("min_samples", 8)
        solve_options.setdefault("residual_threshold", 2)
        solve_options.setdefault("max_trials", 100)
        self._transfo_type = TransformationType(transfo_type)
        self._solver = get_ransac_solver(self._transfo_type, **solve_options)
        super().__init__()

    def calculate(
        self, from_features: Features, to_features: Features
    ) -> NumpyHomography:
        passive = self._solver(to_features.coordinates, from_features.coordinates)
        return NumpyHomography(passive, self._transfo_type)

    def identity(self) -> NumpyHomography:
        return NumpyHomography(numpy.identity(3), TransformationType.identity)


def get_ransac_solver(
    transfo_type: TransformationType, **solve_options
) -> Callable[[Sequence[numpy.ndarray], Sequence[numpy.ndarray]], numpy.ndarray]:
    transfo_type = TransformationType(transfo_type)
    if transfo_type == transfo_type.translation:
        model_classobject = ShiftTransform
    elif transfo_type == transfo_type.rigid:
        model_classobject = EuclideanTransform
    elif transfo_type == transfo_type.similarity:
        model_classobject = SimilarityTransform
    elif transfo_type == transfo_type.affine:
        model_classobject = AffineTransform
    elif transfo_type == transfo_type.projective:
        model_classobject = ProjectiveTransform
    else:
        raise ValueError(f"No ransac solver found for {transfo_type}")

    def ransac_wapper(
        from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
    ) -> numpy.ndarray:
        src = numpy.asarray(from_coord).T
        dst = numpy.asarray(to_coord).T
        tr, inliers = ransac((src, dst), model_classobject, **solve_options)
        return tr.params

    return ransac_wapper
