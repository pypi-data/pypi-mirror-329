import numpy
from .base import Features


class SilxDescriptorFeatures(
    Features, registry_id=Features.RegistryId("Descriptor", "Silx")
):
    def __init__(self, silx_features: numpy.recarray) -> None:
        self._silx_features = silx_features
        self._coordinates = numpy.array([self._silx_features.y, self._silx_features.x])
        self._nfeatures = len(self._silx_features)
        super().__init__()

    def __getitem__(self, idx):
        return type(self)(self._silx_features[idx])

    @property
    def silx_features(self) -> numpy.recarray:
        return self._silx_features

    @property
    def coordinates(self) -> numpy.ndarray:
        return self._coordinates

    @property
    def ndim(self) -> int:
        return 2

    @property
    def nfeatures(self) -> int:
        return self._nfeatures
