from ..transformation.homography import (
    matrix_from_params,
    params_from_trans,
    Homography,
)
import numpy


def test_parameter_conversion():
    matrix = numpy.identity(3)
    trafo = Homography(matrix)
    numpy.testing.assert_allclose(
        trafo.passive,
        matrix_from_params(params_from_trans(trafo), trafo._type.identity),
    )

    matrix[0:2, 2] = [1, 2]
    trafo = Homography(matrix)
    numpy.testing.assert_allclose(
        trafo.passive,
        matrix_from_params(params_from_trans(trafo), trafo._type.translation),
    )

    matrix[0, 0] = numpy.cos(0.1)
    matrix[1, 0] = numpy.sin(0.1)
    matrix[0, 1] = -numpy.sin(0.1)
    matrix[1, 1] = numpy.cos(0.1)
    trafo = Homography(matrix)
    numpy.testing.assert_allclose(
        trafo.passive,
        matrix_from_params(params_from_trans(trafo), trafo._type.rigid),
    )

    matrix[1, 1] *= 1.1
    trafo = Homography(matrix)
    numpy.testing.assert_allclose(
        trafo.passive, matrix_from_params(params_from_trans(trafo), trafo._type.affine)
    )

    matrix[2, 0] = 0.1
    trafo = Homography(matrix)
    numpy.testing.assert_allclose(
        trafo.passive,
        matrix_from_params(params_from_trans(trafo), trafo._type.projective),
    )
