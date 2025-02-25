from ewoksorange.bindings import ows_to_ewoks
from ewokscore import execute_graph

import pytest
import numpy as np

try:
    import Orange.widgets as Orange
except ImportError:
    Orange = None

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


@pytest.mark.skipif(Orange is None, reason="python version not supported by orange")
def test_sp_multi_without_qt(tmpdir):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "sp_multitransfo.ows"
    assert_multi_without_qt(filename, tmpdir)


@pytest.mark.skipif(Orange is None, reason="python version not supported by orange")
def test_sp_multi_with_qt(ewoks_orange_canvas, tmpdir):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "sp_multitransfo.ows"
    assert_multi_with_qt(ewoks_orange_canvas, filename, tmpdir)


def assert_multi_without_qt(filename, tmpdir):
    """Execute workflow after converting it to an ewoks workflow"""
    graph = ows_to_ewoks(filename)
    outputs = execute_graph(
        graph, inputs=[], outputs=[{"all": True}], merge_outputs=False
    )
    expected = outputs["1"]["transformations"]
    for actual in outputs["2"]["transformations"]:
        for ac, ex in zip(actual, expected):
            np.testing.assert_allclose(ac.passive, ex.passive, rtol=0.1, atol=0.05)


def assert_multi_with_qt(ewoks_orange_canvas, filename, tmpdir):
    """Execute workflow using the Qt widgets and signals"""
    ewoks_orange_canvas.load_graph(str(filename), inputs=[])
    ewoks_orange_canvas.start_workflow()
    ewoks_orange_canvas.wait_widgets(timeout=10)
    outputs = {}
    for i in range(1, 4):
        outputs[str(i)] = next(
            ewoks_orange_canvas.widgets_from_name(str(i))
        ).get_task_output_values()
    expected = outputs["1"]["transformations"]
    for actual in outputs["2"]["transformations"]:
        for ac, ex in zip(actual, expected):
            np.testing.assert_allclose(ac.passive, ex.passive, rtol=0.1, atol=0.05)


@pytest.mark.skipif(Orange is None, reason="python version not supported by orange")
def test_sp_single_without_qt(tmpdir):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "sp_singletransfo.ows"
    assert_single_without_qt(filename, tmpdir)


@pytest.mark.skipif(Orange is None, reason="python version not supported by orange")
def test_sp_single_with_qt(ewoks_orange_canvas, tmpdir):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "sp_singletransfo.ows"
    assert_single_with_qt(ewoks_orange_canvas, filename, tmpdir)


def assert_single_without_qt(filename, tmpdir):
    """Execute workflow after converting it to an ewoks workflow"""
    graph = ows_to_ewoks(filename)
    outputs = execute_graph(
        graph, inputs=[], outputs=[{"all": True}], merge_outputs=False
    )

    for ac, ex in zip(outputs["1"]["transformations"], outputs["3"]["transformations"]):
        np.testing.assert_allclose(ac.passive, ex.passive, rtol=0.1, atol=0.05)


def assert_single_with_qt(ewoks_orange_canvas, filename, tmpdir):
    """Execute workflow using the Qt widgets and signals"""
    ewoks_orange_canvas.load_graph(str(filename), inputs=[])
    ewoks_orange_canvas.start_workflow()
    ewoks_orange_canvas.wait_widgets(timeout=10)
    outputs = {}
    for i in range(1, 4):
        outputs[str(i)] = next(
            ewoks_orange_canvas.widgets_from_name(str(i))
        ).get_task_output_values()
    for ac, ex in zip(outputs["1"]["transformations"], outputs["3"]["transformations"]):
        np.testing.assert_allclose(ac.passive, ex.passive, rtol=0.1, atol=0.05)
