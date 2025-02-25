import numpy
from ewoksorange.tests.utils import execute_task

from orangecontrib.ewoksndreg.reg2d_features import OWReg2DFeatures
from orangecontrib.ewoksndreg.reg2d_intensities import OWReg2DIntensities
from orangecontrib.ewoksndreg.reg2d_transform import OWReg2DTransform
from orangecontrib.ewoksndreg.example2d_stack import OWExample2DStack
from orangecontrib.ewoksndreg.reg2d_preeval import OWReg2DPreEvaluation
from .data import data_for_registration
from ..io import output_stack
from ..transformation.numpy_backend import NumpyHomography


def test_owreg2d_features_task(tmpdir):
    _test_owreg2d_features(tmpdir, OWReg2DFeatures.ewokstaskclass)


def test_owreg2d_features_widget(tmpdir, qtapp):
    _test_owreg2d_features(tmpdir, OWReg2DFeatures)


def _test_owreg2d_features(tmpdir, task_cls):
    file_path = str(tmpdir / "data.h5")
    data_path = "entry/instrument/detector/data"
    url = f"silx://{file_path}::{data_path}"
    istack, active1, passive1 = data_for_registration.images("translation", plot=0)
    with output_stack.output_context(url) as stacko:
        stacko.add_points(istack)

    result = execute_task(
        task_cls,
        inputs={
            "imagestack": url,
            "transformation_type": "translation",
            "detector": ("Sift", "SciKitImage"),
            "matcher": ("Descriptor", "SciKitImage"),
            "mapper": ("LstSq", "Numpy"),
        },
    )

    active2 = numpy.stack([tr.active for tr in result["transformations"]])
    passive2 = numpy.stack([tr.passive for tr in result["transformations"]])

    numpy.testing.assert_allclose(active1, active2, rtol=0.01)
    numpy.testing.assert_allclose(passive1, passive2, rtol=0.01)


def test_owreg2d_intensities_task(tmpdir):
    _test_owreg2d_intensities(tmpdir, OWReg2DIntensities.ewokstaskclass)


def test_owreg2d_intensities_widget(tmpdir, qtapp):
    _test_owreg2d_intensities(tmpdir, OWReg2DIntensities)


def _test_owreg2d_intensities(tmpdir, task_cls):
    file_path = str(tmpdir / "data.h5")
    data_path = "entry/instrument/detector/data"
    url = f"silx://{file_path}::{data_path}"
    istack, active1, passive1 = data_for_registration.images("translation", plot=0)
    with output_stack.output_context(url) as stacko:
        stacko.add_points(istack)

    result = execute_task(
        task_cls,
        inputs={
            "imagestack": url,
            "transformation_type": "translation",
            "mapper": ("CrossCorrelation", "Numpy"),
        },
    )

    active2 = numpy.stack([tr.active for tr in result["transformations"]])
    passive2 = numpy.stack([tr.passive for tr in result["transformations"]])

    numpy.testing.assert_allclose(active1, active2, rtol=0.01)
    numpy.testing.assert_allclose(passive1, passive2, rtol=0.01)


def test_owreg2d_intensities_multi_task(tmpdir):
    _test_owreg2d_intensities_multi(tmpdir, OWReg2DIntensities.ewokstaskclass)


def test_owreg2d_intensities_multi_widget(tmpdir, qtapp):
    _test_owreg2d_intensities_multi(tmpdir, OWReg2DIntensities)


def _test_owreg2d_intensities_multi(tmpdir, task_cls):
    file_path = str(tmpdir / "data.h5")
    data_path = "entry/instrument/detector/data"
    url = f"silx://{file_path}::{data_path}"
    istack, active1, passive1 = data_for_registration.images("translation", plot=0)
    istack = [numpy.asarray(istack)] * 3
    with output_stack.output_context(url) as stacko:
        stacko.add_points(istack)

    result = execute_task(
        task_cls,
        inputs={
            "imagestack": url,
            "transformation_type": "translation",
            "mapper": ("CrossCorrelation", "Numpy"),
        },
    )
    for i in range(3):
        active2 = numpy.stack([tr.active for tr in result["transformations"][i]])
        passive2 = numpy.stack([tr.passive for tr in result["transformations"][i]])

        numpy.testing.assert_allclose(active1, active2, rtol=0.01)
        numpy.testing.assert_allclose(passive1, passive2, rtol=0.01)


def test_owreg2d_apply_task():
    _test_owreg2d_apply(OWReg2DTransform.ewokstaskclass)


def test_owreg2d_apply_widget(qtapp):
    _test_owreg2d_apply(OWReg2DTransform)


def _test_owreg2d_apply(task_cls):
    istack, active, passive = data_for_registration.images("translation", plot=0)

    forward = [NumpyHomography(M) for M in passive]
    backward = [NumpyHomography(M) for M in active]

    result = execute_task(
        task_cls,
        inputs={"imagestack": istack, "transformations": forward},
    )
    result = execute_task(
        task_cls,
        inputs={"imagestack": result["imagestack"], "transformations": backward},
    )

    istack = numpy.asarray(istack)
    ostack = numpy.asarray(result["imagestack"])
    ostack[0:9, :] = istack[0:9, :]
    ostack[:, 0:6] = istack[:, 0:6]

    numpy.testing.assert_allclose(istack, ostack)


def test_owreg2d_apply_multi_task():
    _test_owreg2d_apply_multi(OWReg2DTransform.ewokstaskclass)


def test_owreg2d_apply_multi_widget(qtapp):
    _test_owreg2d_apply_multi(OWReg2DTransform)


def _test_owreg2d_apply_multi(task_cls):
    istack, active, passive = data_for_registration.images("translation", plot=0)
    istack = numpy.tile(istack, (4, 1, 1, 1))

    forward = [[NumpyHomography(M) for M in passive]]
    backward = [[NumpyHomography(M) for M in active]]

    result = execute_task(
        task_cls,
        inputs={"imagestack": istack, "transformations": forward},
    )
    result = execute_task(
        task_cls,
        inputs={"imagestack": result["imagestack"], "transformations": backward},
    )

    istack = numpy.asarray(istack)
    ostack = numpy.asarray(result["imagestack"])
    ostack[:, 0:9, :] = istack[:, 0:9, :]
    ostack[:, :, 0:6] = istack[:, :, 0:6]

    numpy.testing.assert_allclose(istack, ostack)


def test_owexample2d_stack_task():
    _test_owexample2d_stack(OWExample2DStack.ewokstaskclass)


def test_owexample2d_stack_widget(qtapp):
    _test_owexample2d_stack(OWExample2DStack.ewokstaskclass)


def _test_owexample2d_stack(task_cls):
    istack, active, passive = data_for_registration.images("translation", plot=0)

    result = execute_task(
        task_cls,
        inputs={"name": "astronaut", "transformation_type": "translation"},
    )

    istack = numpy.asarray(istack)
    ostack = numpy.asarray(result["imagestack"])
    numpy.testing.assert_allclose(istack, ostack)

    for tr, a, p in zip(result["transformations"], active, passive):
        numpy.testing.assert_allclose(tr.active, a)
        numpy.testing.assert_allclose(tr.passive, p)


def test_owreg2d_preeval_widget(tmpdir):
    _test_owreg2d_preeval(tmpdir, OWReg2DPreEvaluation)


def test_owreg2d_preeval_task(tmpdir):
    _test_owreg2d_preeval(tmpdir, OWReg2DPreEvaluation.ewokstaskclass)


def _test_owreg2d_preeval(tmpdir, task_cls):
    file_path = str(tmpdir / "data.h5")
    data_path = "entry/instrument/detector/data"
    url = f"silx://{file_path}::{data_path}"
    istack = data_for_registration.noisy_imagestacks("rigid", nstacks=4)

    with output_stack.output_context(url) as stacko:
        stacko.add_points(istack)

    result = execute_task(
        task_cls,
        inputs={
            "imagestacks": url,
        },
    )
    numpy.testing.assert_equal(result["ranking"], [0, 1, 2, 3])
