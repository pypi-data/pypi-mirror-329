import numpy
from ..transformation.homography import type_from_matrix
from ..transformation.types import TransformationType


def test_type_from_matrix():
    matrix = numpy.identity(3)
    assert type_from_matrix(matrix) == TransformationType.identity

    matrix[0:2, 2] = [1, 2]
    assert type_from_matrix(matrix) == TransformationType.translation

    matrix[0, 0] = numpy.cos(0.1)
    matrix[1, 0] = numpy.sin(0.1)
    matrix[0, 1] = -numpy.sin(0.1)
    matrix[1, 1] = numpy.cos(0.1)
    assert type_from_matrix(matrix) == TransformationType.rigid

    matrix[0, 0] *= 1.1
    matrix[1, 1] *= 1.1
    assert type_from_matrix(matrix) == TransformationType.similarity

    matrix[1, 1] *= 1.1
    assert type_from_matrix(matrix) == TransformationType.affine

    matrix[2, 0] = 0.1
    assert type_from_matrix(matrix) == TransformationType.projective
