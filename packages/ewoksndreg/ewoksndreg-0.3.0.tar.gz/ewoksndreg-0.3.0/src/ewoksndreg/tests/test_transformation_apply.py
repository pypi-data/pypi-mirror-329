import numpy
from ..transformation import apply_transformations
from ..transformation.homography import Homography
from ..io.input_stack import InputStackNumpy
from ..io.output_stack import OutputStackNumpy
from .data import data_for_registration
import pytest

_HOMOGRAPHIES = {
    f"homography{'_'.join(k)}": v for k, v in Homography.get_subclass_items()
}


@pytest.mark.parametrize("homography", _HOMOGRAPHIES)
def test_apply_transformations(homography):
    istack, active, passive = data_for_registration.images("translation", plot=0)

    forward = [_HOMOGRAPHIES[homography](passive=M) for M in passive]
    backward = [_HOMOGRAPHIES[homography](passive=M) for M in active]

    data1 = list()
    with OutputStackNumpy(data1) as ostack:
        apply_transformations(istack, ostack, forward, interpolation_order=0)

    data2 = list()
    with OutputStackNumpy(data2) as ostack:
        with InputStackNumpy(data1) as istack2:
            apply_transformations(istack2, ostack, backward, interpolation_order=0)

    istack = numpy.asarray(istack)
    ostack = numpy.asarray(data2)
    idx = numpy.isnan(ostack)
    ostack[idx] = istack[idx]

    numpy.testing.assert_allclose(istack, ostack)


@pytest.mark.parametrize("homography", _HOMOGRAPHIES)
def test_apply_translation(homography):
    image = numpy.random.uniform(0.0, 10, (10, 10))

    transform = numpy.array([[1, 0, 6], [0, 1, -2], [0, 0, 1]], dtype=numpy.float64)
    forward = _HOMOGRAPHIES[homography](passive=transform)
    goal = numpy.zeros((10, 10))
    goal[0:4, 2:10] = image[6:10, 0:8]
    actual = forward.apply_data(image, cval=0)

    numpy.testing.assert_allclose(actual, goal)


@pytest.mark.parametrize("homography", _HOMOGRAPHIES)
def test_apply_coordinate(homography):
    nx, ny = numpy.meshgrid(numpy.arange(4, dtype=numpy.float64), numpy.arange(4))
    nx, ny = nx.flatten(), ny.flatten()
    matrix = numpy.identity(3)
    matrix[0:2, 2] = [-1, -3]

    forward = _HOMOGRAPHIES[homography](passive=matrix)
    res1 = forward.apply_coordinates(numpy.asarray([nx, ny]))
    numpy.testing.assert_allclose([nx + 1, ny + 3], res1)

    matrix = numpy.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=numpy.float64)

    forward = _HOMOGRAPHIES[homography](passive=matrix)
    res1 = forward.apply_coordinates(numpy.asarray([nx, ny]))

    numpy.testing.assert_allclose([ny, -nx], res1, atol=numpy.finfo(numpy.float64).eps)
