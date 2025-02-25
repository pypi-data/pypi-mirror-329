import numpy
from ..features.features import NumpyKeypointFeatures
from ..features.matching.numpy_backend import match_keypoints
from .data import data_for_registration


def test_match_keypoints():
    image = data_for_registration.images("translation", nimages=1)[0][0]
    rs = numpy.random.RandomState(seed=100)
    p0 = rs.uniform(0, image.shape[0], 10)
    p1 = rs.uniform(0, image.shape[1], 10)
    coordinates = numpy.array([p0, p1])
    features1 = NumpyKeypointFeatures(coordinates.T)

    ridx = numpy.arange(10)
    rs.shuffle(ridx)
    features2 = NumpyKeypointFeatures(coordinates.T[ridx])

    idx = match_keypoints(features1, features1, image, image)
    idx1, idx2 = idx.T
    sidx = numpy.argsort(idx1)
    numpy.testing.assert_array_equal(idx1[sidx], numpy.arange(10))
    numpy.testing.assert_array_equal(idx2[sidx], numpy.arange(10))

    idx = match_keypoints(features1, features2, image, image)
    idx1, idx2 = idx.T
    sidx = numpy.argsort(idx1)
    numpy.testing.assert_array_equal(idx1[sidx], numpy.arange(10))
    numpy.testing.assert_array_equal(idx2[sidx], numpy.argsort(ridx))
