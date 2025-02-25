import numpy
from .base import Features


class SciKitImageDescriptorFeatures(
    Features, registry_id=Features.RegistryId("Descriptor", "SciKitImage")
):
    def __init__(self, keypoints: numpy.ndarray, descriptors: numpy.ndarray) -> None:
        nfeatures, ndim = keypoints.shape
        if ndim != 2:
            raise ValueError("only 2D features are supported")
        self._descriptors = descriptors  # nfeatures x descriptor_size
        self._keypoints = keypoints
        self._coordinates = keypoints.T
        self._nfeatures = nfeatures
        super().__init__()

    def __getitem__(self, idx):
        return type(self)(self._keypoints[idx], self._descriptors[idx])

    @property
    def skimage_keypoints(self) -> numpy.ndarray:
        return self._keypoints

    @property
    def skimage_descriptors(self) -> numpy.ndarray:
        return self._descriptors

    @property
    def coordinates(self) -> numpy.ndarray:
        return self._coordinates

    @property
    def ndim(self) -> int:
        return 2

    @property
    def nfeatures(self) -> int:
        return self._nfeatures
