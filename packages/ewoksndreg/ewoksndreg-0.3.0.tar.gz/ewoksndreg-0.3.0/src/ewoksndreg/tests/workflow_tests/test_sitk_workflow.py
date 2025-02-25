from typing import List
from ewoksorange.bindings import ows_to_ewoks
from ewokscore import execute_graph

import numpy as np
import pytest

try:
    import SimpleITK as sitk
except ImportError:
    sitk = None

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


@pytest.mark.skipif(
    sitk is None, reason="Workflow uses SimpleITK, which is not available"
)
def test_rigid_workflow_without_qt(tmpdir):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "sitk.ows"
    assert_workflow_without_qt(filename, tmpdir)


@pytest.mark.skipif(
    sitk is None, reason="Workflow uses SimpleITK, which is not available"
)
def test_rigid_workflow_with_qt(ewoks_orange_canvas, tmpdir):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "sitk.ows"
    assert_workflow_with_qt(ewoks_orange_canvas, filename, tmpdir)


def assert_workflow_without_qt(filename, tmpdir):
    """Execute workflow after converting it to an ewoks workflow"""
    graph = ows_to_ewoks(filename)
    outputs = execute_graph(
        graph, inputs=get_inputs(tmpdir), outputs=[{"all": True}], merge_outputs=False
    )
    for actual, expected in zip(
        outputs["2"]["transformations"], outputs["3"]["transformations"]
    ):
        np.testing.assert_allclose(
            actual.passive, expected.passive, rtol=0.1, atol=0.05
        )
    for actual, expected in zip(outputs["1"]["imagestack"], outputs["0"]["imagestack"]):
        expected = expected[1 - np.isnan(actual)]
        actual = actual[1 - np.isnan(actual)]
        np.testing.assert_allclose(actual, expected, rtol=0.1, atol=0.05)


def assert_workflow_with_qt(ewoks_orange_canvas, filename, tmpdir):
    """Execute workflow using the Qt widgets and signals"""
    ewoks_orange_canvas.load_graph(str(filename), inputs=get_inputs(tmpdir))
    ewoks_orange_canvas.start_workflow()
    ewoks_orange_canvas.wait_widgets(timeout=10)
    outputs = dict(ewoks_orange_canvas.iter_output_values())
    for actual, expected in zip(
        outputs["2"]["transformations"], outputs["3"]["transformations"]
    ):
        np.testing.assert_allclose(
            actual.passive, expected.passive, rtol=0.1, atol=0.05
        )
    for actual, expected in zip(outputs["1"]["imagestack"], outputs["0"]["imagestack"]):
        expected = expected[1 - np.isnan(actual)]
        actual = actual[1 - np.isnan(actual)]
        np.testing.assert_allclose(actual, expected, rtol=0.1, atol=0.05)


def get_inputs(tmpdir) -> List[dict]:
    return []
