from typing import Tuple, Optional, Mapping
from skimage.feature import match_descriptors
from .base import FeatureMatching
from ..features import Features
from ..features import SciKitImageDescriptorFeatures

__all__ = ["SciKitImageDescriptorFeatureMatching"]


class SciKitImageDescriptorFeatureMatching(
    FeatureMatching, registry_id=FeatureMatching.RegistryId("Descriptor", "SciKitImage")
):
    def __init__(self, match_options: Optional[Mapping] = None, **kw) -> None:
        if match_options is None:
            match_options = dict()
        self._match_options = match_options
        super().__init__(**kw)

    def match(
        self, from_features: Features, to_features: Features, *_
    ) -> Tuple[Features, Features]:
        sk_from_features = from_features.as_type(SciKitImageDescriptorFeatures)
        sk_to_features = to_features.as_type(SciKitImageDescriptorFeatures)
        idx_from, idx_to = match_descriptors(
            sk_from_features.skimage_descriptors,
            sk_to_features.skimage_descriptors,
            **self._match_options,
        ).T
        return (from_features[idx_from], to_features[idx_to])
