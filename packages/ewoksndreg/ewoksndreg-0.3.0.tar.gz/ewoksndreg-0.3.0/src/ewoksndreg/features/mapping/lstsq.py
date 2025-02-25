"""Calculate active transformation between two sets of coordinates"""

from typing import Sequence, Callable, Dict
import numpy
from ...transformation import lstsq
from ...transformation import TransformationType


_METHODS: Dict[
    TransformationType,
    Callable[[Sequence[numpy.ndarray], Sequence[numpy.ndarray]], numpy.ndarray],
] = {
    TransformationType.identity: lstsq.calc_identity,
    TransformationType.translation: lstsq.calc_translation,
    TransformationType.rigid: lstsq.calc_rigid,
    TransformationType.similarity: lstsq.calc_similarity,
    TransformationType.affine: lstsq.calc_affine,
    TransformationType.projective: lstsq.calc_projective,
}


def get_lstsq_solver(
    transfo_type: TransformationType,
) -> Callable[[Sequence[numpy.ndarray], Sequence[numpy.ndarray]], numpy.ndarray]:
    try:
        return _METHODS[transfo_type]
    except KeyError:
        raise ValueError(f"No least-squares solver found for {transfo_type}") from None
