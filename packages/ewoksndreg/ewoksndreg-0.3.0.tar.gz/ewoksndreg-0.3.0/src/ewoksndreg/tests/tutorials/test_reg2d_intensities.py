from typing import List, Dict
from ewoksorange.bindings import ows_to_ewoks
from ewokscore import execute_graph

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


def test_reg2d_intensities_without_qt(tmpdir):
    from orangecontrib.ewoksndreg import tutorials

    filename = resource_files(tutorials) / "reg2d_intensities.ows"
    assert_reg2d_intensities_without_qt(filename, tmpdir)


def test_reg2d_intensities_with_qt(ewoks_orange_canvas, tmpdir):
    from orangecontrib.ewoksndreg import tutorials

    filename = resource_files(tutorials) / "reg2d_intensities.ows"
    assert_reg2d_intensities_with_qt(ewoks_orange_canvas, filename, tmpdir)


def assert_reg2d_intensities_without_qt(filename, tmpdir):
    """Execute workflow after converting it to an ewoks workflow"""
    graph = ows_to_ewoks(filename)
    outputs = execute_graph(
        graph, inputs=get_inputs(tmpdir), outputs=[{"all": True}], merge_outputs=False
    )
    expected = get_expected_outputs(tmpdir)
    label_to_id = {
        attrs["label"]: node_id for node_id, attrs in graph.graph.nodes.items()
    }
    outputs = {k: set(v) for k, v in outputs.items()}
    expected = {label_to_id[k]: v for k, v in expected.items()}
    assert outputs == expected


def assert_reg2d_intensities_with_qt(ewoks_orange_canvas, filename, tmpdir):
    """Execute workflow using the Qt widgets and signals"""
    ewoks_orange_canvas.load_graph(str(filename), inputs=get_inputs(tmpdir))
    ewoks_orange_canvas.start_workflow()
    ewoks_orange_canvas.wait_widgets(timeout=10)
    outputs = dict(ewoks_orange_canvas.iter_output_values())
    outputs = {k: set(v) for k, v in outputs.items()}
    assert outputs == get_expected_outputs(tmpdir)


def get_inputs(tmpdir) -> List[dict]:
    return list()


def get_expected_outputs(tmpdir) -> Dict[str, dict]:
    return {
        "Align (theory)": {"imagestack"},
        "2D Intensity-Based Registration": {"transformations"},
        "Align": {"imagestack"},
        "2D Example Stack": {"imagestack", "transformations"},
    }
