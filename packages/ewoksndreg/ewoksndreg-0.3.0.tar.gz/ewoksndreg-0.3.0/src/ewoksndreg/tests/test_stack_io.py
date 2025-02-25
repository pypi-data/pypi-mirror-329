import numpy
from silx.io import get_data
from ..io import input_stack
from ..io import output_stack


def test_stack_io_numpy():
    values = numpy.zeros((2, 3))
    expected = [values, values + 1, values + 2]

    data = list()
    with output_stack.OutputStackNumpy(data) as stacko:
        stacko.add_point(values)
        stacko.add_points([values + 1, values + 2])
    numpy.testing.assert_array_equal(expected, data)

    with output_stack.output_context() as stacko:
        stacko.add_point(values)
        stacko.add_points([values + 1, values + 2])
        result = stacko.data
    numpy.testing.assert_array_equal(expected, result)

    with input_stack.InputStackNumpy(data) as stacki:
        result = numpy.stack(stacki, axis=0)
    numpy.testing.assert_array_equal(expected, result)

    with input_stack.input_context(data) as stacki:
        result = numpy.stack(stacki, axis=0)
    numpy.testing.assert_array_equal(expected, result)

    with input_stack.InputStackNumpy([data, data], inputs_are_stacks=True) as stacki:
        result = numpy.stack(stacki, axis=0)
    numpy.testing.assert_array_equal(expected + expected, result)

    with input_stack.input_context([data, data], inputs_are_stacks=True) as stacki:
        result = numpy.stack(stacki, axis=0)
    numpy.testing.assert_array_equal(expected + expected, result)


def test_stack_io_hdf5(tmpdir):
    file_path = str(tmpdir / "data1.h5")
    data_path = "entry/instrument/detector/data"
    uri = f"silx://{file_path}::{data_path}"

    values = numpy.zeros((2, 3))
    expected = [values, values + 1, values + 2]

    with output_stack.OutputStackHdf5(uri) as stacko:
        stacko.add_point(values)
        stacko.add_points([values + 1, values + 2])
    numpy.testing.assert_array_equal(expected, get_data(uri))

    file_path = str(tmpdir / "data2.h5")
    uri = f"silx://{file_path}::{data_path}"

    with output_stack.output_context(uri) as stacko:
        stacko.add_point(values)
        stacko.add_points([values + 1, values + 2])
    numpy.testing.assert_array_equal(expected, get_data(uri))

    with input_stack.InputStackHdf5(uri) as stacki:
        data = numpy.stack(list(stacki), axis=0)
    numpy.testing.assert_array_equal(expected, data)

    with input_stack.input_context(uri) as stacki:
        data = numpy.stack(list(stacki), axis=0)
    numpy.testing.assert_array_equal(expected, data)

    with input_stack.InputStackHdf5([uri, uri], inputs_are_stacks=True) as stacki:
        data = numpy.stack(list(stacki), axis=0)
    numpy.testing.assert_array_equal(expected + expected, data)

    with input_stack.input_context([uri, uri], inputs_are_stacks=True) as stacki:
        data = numpy.stack(list(stacki), axis=0)
    numpy.testing.assert_array_equal(expected + expected, data)
