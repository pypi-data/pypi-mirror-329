import numpy
import pytest
from ..intensities import registration
from ..io.input_stack import InputStackNumpy
from .data import data_for_registration
from ..transformation.homography import Homography
from ..transformation.numpy_backend import NumpyHomography

_MAPPERS = {
    f"mapper{'_'.join(k)}": v
    for k, v in registration.IntensityMapping.get_subclass_items()
}


@pytest.mark.parametrize("mapper", _MAPPERS)
@pytest.mark.parametrize(
    "transfo_type",
    ["translation", "rigid", "affine", "similarity"],
)
def test_intensity_registration(transfo_type, mapper):
    if transfo_type not in _MAPPERS[mapper].SUPPORTED_TRANSFORMATIONS:
        pytest.skip(f"transformation type {transfo_type} not supported by {mapper}")

    istack, active1, passive1 = data_for_registration.images(transfo_type, plot=0)
    istack = InputStackNumpy(istack)

    mapper = _MAPPERS[mapper](transfo_type=transfo_type)

    transformations = registration.calculate_transformations(istack, mapper)

    if isinstance(transformations[0], Homography):
        active2 = numpy.stack([tr.active for tr in transformations])
        passive2 = numpy.stack([tr.passive for tr in transformations])
        numpy.testing.assert_allclose(active1, active2, rtol=0.1, atol=0.1)
        numpy.testing.assert_allclose(passive1, passive2, rtol=0.1, atol=0.1)

    nx, ny = numpy.mgrid[0:100:10, 0:100:10]
    nx, ny = nx.astype(numpy.float64), ny.astype(numpy.float64)

    for i, transformation in enumerate(transformations):
        res1 = transformation.apply_coordinates(
            numpy.asarray([nx.flatten(), ny.flatten()])
        )
        res2 = NumpyHomography(passive1[i]).apply_coordinates(
            numpy.asarray([nx.flatten(), ny.flatten()])
        )
        numpy.testing.assert_allclose(res1, res2, rtol=0.1, atol=0.4)


@pytest.mark.parametrize("mapper", _MAPPERS)
@pytest.mark.parametrize("transfo_type", ["translation", "affine"])
def test_intensity_registration_block(transfo_type, mapper):
    if transfo_type in _MAPPERS[mapper].SUPPORTED_TRANSFORMATIONS:
        istack, active1, passive1 = data_for_registration.images(
            transfo_type, nimages=7, plot=0
        )
        istack = InputStackNumpy(istack)

        mapper = _MAPPERS[mapper](transfo_type=transfo_type)

        transformations = registration.calculate_transformations(
            istack, mapper, include=[0, 1, 2, 4, 5, 6], reference=0, block_size=3
        )
        active1.pop(3)
        passive1.pop(3)
        if isinstance(transformations[0], Homography):
            active2 = numpy.stack([tr.active for tr in transformations])
            passive2 = numpy.stack([tr.passive for tr in transformations])
            numpy.testing.assert_allclose(active1, active2, rtol=0.01, atol=0.1)
            numpy.testing.assert_allclose(passive1, passive2, rtol=0.01, atol=0.1)

        nx, ny = numpy.mgrid[0:100:10, 0:100:10]
        nx, ny = nx.astype(numpy.float64), ny.astype(numpy.float64)

        for i, transformation in enumerate(transformations):
            res1 = transformation.apply_coordinates(
                numpy.asarray([nx.flatten(), ny.flatten()])
            )
            res2 = NumpyHomography(passive1[i]).apply_coordinates(
                numpy.asarray([nx.flatten(), ny.flatten()])
            )
            numpy.testing.assert_allclose(res1, res2, rtol=0.1, atol=0.4)
