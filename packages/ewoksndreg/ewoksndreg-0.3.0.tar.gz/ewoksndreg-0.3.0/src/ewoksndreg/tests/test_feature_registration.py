import numpy
import pytest
from ..features import registration
from ..io.input_stack import InputStackNumpy
from .data import data_for_registration


_DETECTORS = {
    f"detector{'_'.join(k)}": v
    for k, v in registration.FeatureDetector.get_subclass_items()
}
_MATCHERS = {
    f"matcher{'_'.join(k)}": v
    for k, v in registration.FeatureMatching.get_subclass_items()
}
_MAPPERS = {
    f"mapper{'_'.join(k)}": v
    for k, v in registration.FeatureMapping.get_subclass_items()
}


@pytest.mark.parametrize("mapper", _MAPPERS)
@pytest.mark.parametrize("detector", _DETECTORS)
@pytest.mark.parametrize("matcher", _MATCHERS)
@pytest.mark.parametrize("transfo_type", ["translation"])
def test_feature_registration(transfo_type, matcher, detector, mapper):
    istack, active1, passive1 = data_for_registration.images(transfo_type, plot=0)
    istack = InputStackNumpy(istack)

    detector = _DETECTORS[detector]()
    matcher = _MATCHERS[matcher]()
    mapper = _MAPPERS[mapper](transfo_type)

    transformations = registration.calculate_transformations(
        istack, detector, matcher, mapper
    )

    active2 = numpy.stack([tr.active for tr in transformations])
    passive2 = numpy.stack([tr.passive for tr in transformations])

    if "Sift" in detector.get_subclass_id():
        rtol = 0.01
    else:
        rtol = 0.05
    numpy.testing.assert_allclose(active1, active2, rtol=rtol)
    numpy.testing.assert_allclose(passive1, passive2, rtol=rtol)
