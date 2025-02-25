from typing import List
from ewoksorange.bindings import ows_to_ewoks
from ewokscore import execute_graph

import numpy as np
import pytest

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


pytestmark = pytest.mark.parametrize(
    "reference, block_size",
    [
        (0, 0),
        (29, 1000),
        (59, 5),
        (13, 3),
        pytest.param(0, 1000, marks=pytest.mark.xfail),
    ],
)


def test_strat_workflow_without_qt(tmpdir, reference, block_size):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "strategy.ows"
    assert_workflow_without_qt(filename, tmpdir, reference, block_size)


def test_strat_workflow_with_qt(ewoks_orange_canvas, tmpdir, reference, block_size):
    from ewoksndreg.tests.workflow_tests import workflows

    filename = resource_files(workflows) / "strategy.ows"
    assert_workflow_with_qt(
        ewoks_orange_canvas, filename, tmpdir, reference, block_size
    )


def assert_workflow_without_qt(filename, tmpdir, reference, block_size):
    """Execute workflow after converting it to an ewoks workflow"""
    graph = ows_to_ewoks(filename)
    outputs = execute_graph(
        graph,
        inputs=get_inputs(tmpdir, reference, block_size),
        outputs=[{"all": True}],
        merge_outputs=False,
    )
    expected = outputs["0"]["imagestack"][reference]
    for actual in outputs["2"]["imagestack"]:
        expected_flat = expected[np.isfinite(actual)]
        actual_flat = actual[np.isfinite(actual)]
        np.testing.assert_allclose(actual_flat, expected_flat, rtol=0.1, atol=0.05)


def assert_workflow_with_qt(
    ewoks_orange_canvas, filename, tmpdir, reference, block_size
):
    """Execute workflow using the Qt widgets and signals"""
    ewoks_orange_canvas.load_graph(str(filename), inputs=[])
    ewoks_orange_canvas.set_input_values(get_inputs(tmpdir, reference, block_size))
    ewoks_orange_canvas.start_workflow()
    ewoks_orange_canvas.wait_widgets(timeout=10)
    outputs = dict(ewoks_orange_canvas.iter_output_values())
    expected = outputs["0"]["imagestack"][reference]
    for actual in outputs["2"]["imagestack"]:
        expected_flat = expected[np.isfinite(actual)]
        actual_flat = actual[np.isfinite(actual)]
        np.testing.assert_allclose(actual_flat, expected_flat, rtol=0.1, atol=0.05)


def get_inputs(tmpdir, reference, block_size) -> List[dict]:
    return [
        {
            "label": "1",
            "name": "reference",
            "value": reference,
        },
        {
            "label": "1",
            "name": "block_size",
            "value": block_size,
        },
    ]
