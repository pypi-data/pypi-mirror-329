from typing import Optional, Mapping
import numpy
from skimage.feature import SIFT, ORB, BRIEF, CENSURE
from skimage.feature import corner_harris, corner_subpix, corner_peaks
from .base import FeatureDetector
from ..features import SciKitImageDescriptorFeatures

__all__ = ["SciKitImageSiftFeatureDetector"]


class SciKitImageSiftFeatureDetector(
    FeatureDetector, registry_id=FeatureDetector.RegistryId("Sift", "SciKitImage")
):
    def __init__(self, feature_options: Optional[Mapping] = None, **kw) -> None:
        if feature_options is None:
            feature_options = dict()
        self._feature_detector = SIFT(**feature_options)
        super().__init__(**kw)

    def find(self, image: numpy.ndarray) -> SciKitImageDescriptorFeatures:
        self._feature_detector.detect_and_extract(image)
        keypoints = self._feature_detector.keypoints
        descriptors = self._feature_detector.descriptors

        if self._mask is not None:
            masked = _mask_keypoints(self._mask, keypoints)
            keypoints = keypoints[masked]
            descriptors = descriptors[masked]

        return SciKitImageDescriptorFeatures(keypoints, descriptors)


class SciKitImageOrbFeatureDetector(
    FeatureDetector, registry_id=FeatureDetector.RegistryId("Orb", "SciKitImage")
):
    def __init__(self, feature_options: Optional[Mapping] = None, **kw) -> None:
        if feature_options is None:
            feature_options = dict()
        self._feature_detector = ORB(**feature_options)
        super().__init__(**kw)

    def find(self, image: numpy.ndarray) -> SciKitImageDescriptorFeatures:
        self._feature_detector.detect_and_extract(image)
        keypoints = self._feature_detector.keypoints
        descriptors = self._feature_detector.descriptors

        if self._mask is not None:
            masked = _mask_keypoints(self._mask, keypoints)
            keypoints = keypoints[masked]
            descriptors = descriptors[masked]

        return SciKitImageDescriptorFeatures(keypoints, descriptors)


class SciKitImageCensureFeatureDetector(
    FeatureDetector,
    registry_id=FeatureDetector.RegistryId("Censure", "SciKitImage"),
    register=False,
):
    def __init__(
        self,
        feature_options: Optional[Mapping] = None,
        descriptor_options: Optional[Mapping] = None,
        **kw,
    ) -> None:
        if feature_options is None:
            feature_options = dict()
        if descriptor_options is None:
            descriptor_options = dict()
        self._feature_detector = CENSURE(**feature_options)
        self._descriptor_extractor = BRIEF(**descriptor_options)
        super().__init__(**kw)

    def find(self, image: numpy.ndarray) -> SciKitImageDescriptorFeatures:
        self._feature_detector.detect(image)
        keypoints = self._feature_detector.keypoints
        if self._mask is not None:
            masked = _mask_keypoints(self._mask, keypoints)
            keypoints = keypoints[masked]
        self._descriptor_extractor.extract(image, keypoints)
        return SciKitImageDescriptorFeatures(
            keypoints, self._descriptor_extractor.descriptors
        )


class SciKitImageHarrisFeatureDetector(
    FeatureDetector,
    registry_id=FeatureDetector.RegistryId("Harris", "SciKitImage"),
    register=False,
):
    def __init__(
        self,
        feature_options: Optional[Mapping] = None,
        descriptor_options: Optional[Mapping] = None,
        **kw,
    ) -> None:
        if feature_options is None:
            feature_options = dict()
        feature_options.setdefault("min_distance", 5)
        feature_options.setdefault("threshold_rel", 0.01)
        if descriptor_options is None:
            descriptor_options = dict()
        self._feature_options = feature_options
        self._descriptor_extractor = BRIEF(**descriptor_options)
        super().__init__(**kw)

    def find(self, image: numpy.ndarray) -> SciKitImageDescriptorFeatures:
        keypoints = corner_peaks(corner_harris(image), **self._feature_options)
        keypoints = corner_subpix(image, keypoints, window_size=9)
        keypoints = keypoints[~numpy.isnan(keypoints[:, 0])]
        if self._mask is not None:
            masked = _mask_keypoints(self._mask, keypoints)
            keypoints = keypoints[masked]
        self._descriptor_extractor.extract(image, keypoints)
        return SciKitImageDescriptorFeatures(
            keypoints, self._descriptor_extractor.descriptors
        )


def _mask_keypoints(mask: numpy.ndarray, keypoints: numpy.ndarray):
    kp0 = numpy.round(keypoints[:, 0]).astype(numpy.int32)
    kp1 = numpy.round(keypoints[:, 1]).astype(numpy.int32)
    return mask[(kp0, kp1)].astype(bool)
