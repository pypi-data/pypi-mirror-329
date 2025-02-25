import pytest
from .data import data_for_registration
import numpy
from ..transformation.scikitimage_backend import SciKitImageHomography


@pytest.mark.parametrize(
    "transfo_type", ["translation", "rigid", "similarity", "affine"]
)
def test_images(transfo_type):
    data_for_registration.images(transfo_type, plot=0)


@pytest.mark.parametrize("transfo_type", ["rigid", "similarity", "affine"])
def test_transformations(transfo_type):
    images, active, passive = data_for_registration.images(
        transfo_type, nimages=5, name="gravel", plot=0
    )
    back = [
        SciKitImageHomography(passive=mat, warp_options={"order": 3}) for mat in passive
    ]
    results = [hom.apply_data(images[i]) for i, hom in enumerate(back)]

    diffs = [(images[0] - res) for res in results]

    numpy.testing.assert_allclose(numpy.nanmax(diffs, axis=(1, 2)), 0, atol=0.2)
