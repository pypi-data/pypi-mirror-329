"""Data features in n-D datasets"""

import numpy
from .base import Features
from .numpy_backend import NumpyKeypointFeatures

try:
    from .silx_backend import SilxDescriptorFeatures  # noqa F401
except ImportError:
    pass

try:
    from .scikitimage_backend import SciKitImageDescriptorFeatures  # noqa F401
except ImportError:
    pass


def _to_numpy_keypoint_features(features: Features) -> NumpyKeypointFeatures:
    return NumpyKeypointFeatures(numpy.asarray(features.coordinates).T)


for cls in Features.get_subclasses():
    if cls is not NumpyKeypointFeatures:
        cls._set_feature_type_converter(
            NumpyKeypointFeatures, _to_numpy_keypoint_features
        )


try:

    def _scikitimage_to_silx_descriptor(
        skimage_features: SciKitImageDescriptorFeatures,
    ) -> SilxDescriptorFeatures:
        desc = skimage_features.skimage_descriptors
        y, x = skimage_features.coordinates

        desc_shape = desc.shape
        if desc_shape[1] != 128:
            desc = desc.reshape((desc_shape[0], 128, desc_shape[1] // 128))
            desc = desc.astype(numpy.uint8)
            desc = desc.sum(axis=-1)

        dtype = numpy.dtype(
            [
                ("x", numpy.float32),
                ("y", numpy.float32),
                ("scale", numpy.float32),
                ("angle", numpy.float32),
                ("desc", (numpy.uint8, 128)),
            ]
        )

        n = len(desc)
        silx_features = numpy.recarray(shape=(n,), dtype=dtype)
        zeros = numpy.zeros(n, numpy.float32)
        silx_features[:].x = x.astype(numpy.float32)
        silx_features[:].y = y.astype(numpy.float32)
        silx_features[:].scale = zeros
        silx_features[:].angle = zeros
        silx_features[:].desc = desc.astype(numpy.uint8)
        return SilxDescriptorFeatures(silx_features)

    def _silx_to_scikitimage_descriptor(
        silx_features: SilxDescriptorFeatures,
    ) -> SciKitImageDescriptorFeatures:
        keypoints = silx_features.coordinates.T
        descriptors = silx_features.silx_features.desc
        return SciKitImageDescriptorFeatures(keypoints, descriptors)

    SciKitImageDescriptorFeatures._set_feature_type_converter(
        SilxDescriptorFeatures, _scikitimage_to_silx_descriptor
    )
    SilxDescriptorFeatures._set_feature_type_converter(
        SciKitImageDescriptorFeatures, _silx_to_scikitimage_descriptor
    )

except NameError:
    pass
