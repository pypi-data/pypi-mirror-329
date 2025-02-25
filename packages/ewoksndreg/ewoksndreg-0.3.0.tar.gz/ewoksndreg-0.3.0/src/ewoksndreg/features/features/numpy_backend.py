import numpy
from .base import Features


__all__ = ["NumpyKeypointFeatures"]


class NumpyKeypointFeatures(
    Features, registry_id=Features.RegistryId("Keypoints", "Numpy")
):
    def __init__(self, keypoints: numpy.ndarray) -> None:
        nfeatures, ndim = keypoints.shape
        self._coordinates = keypoints.T
        self._ndim = ndim
        self._nfeatures = nfeatures
        super().__init__()

    def __getitem__(self, idx):
        return type(self)(self.keypoints[idx])

    @property
    def keypoints(self) -> numpy.ndarray:
        return self._keypoints

    @property
    def coordinates(self) -> numpy.ndarray:
        return self._coordinates

    @property
    def ndim(self) -> int:
        return self._ndim

    @property
    def nfeatures(self) -> int:
        return self._nfeatures
