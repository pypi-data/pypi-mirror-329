from typing import Optional, Mapping
import numpy
from silx.opencl.common import ocl
from silx.opencl import sift
from .base import FeatureDetector
from ..features import SilxDescriptorFeatures

if ocl is None:
    raise ImportError("pyopencl missing")

__all__ = ["SilxSiftFeatureDetector"]


class SilxSiftFeatureDetector(
    FeatureDetector, registry_id=FeatureDetector.RegistryId("Sift", "Silx")
):
    def __init__(self, feature_options: Optional[Mapping] = None, **kw) -> None:
        if feature_options is None:
            feature_options = dict()
        self._feature_options = feature_options
        self._feature_detector = None
        super().__init__(**kw)

    def find(self, image: numpy.ndarray) -> SilxDescriptorFeatures:
        if (
            self._feature_detector is None
            or self._feature_detector.dtype is not image.dtype
            or self._feature_detector.shape != image.shape
        ):
            self._feature_detector = sift.SiftPlan(
                dtype=image.dtype, shape=image.shape, **self._feature_options
            )
        silx_features = self._feature_detector.keypoints(image)

        if self._mask is not None:
            kpx = numpy.round(silx_features.x).astype(numpy.int32)
            kpy = numpy.round(silx_features.y).astype(numpy.int32)
            masked = self._mask[(kpy, kpx)].astype(bool)
            silx_features = silx_features[masked]

        return SilxDescriptorFeatures(silx_features)
