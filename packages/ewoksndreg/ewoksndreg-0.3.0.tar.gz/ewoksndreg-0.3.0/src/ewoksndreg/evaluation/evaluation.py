import numpy as np
from typing import List

from ..io.input_stack import InputStack
from .eval_metrics import peak_eval, smoothness_eval, mse_eval
from ..transformation.homography import Homography


def pre_evaluation(stacks: InputStack):
    """
    Evaluates what the most successful stacks for registration might be.

    param stacks: list of imagestacks of the same image

    returns: indices of the most promising stacks for registration
    """
    evals = list()
    for stack in stacks:
        evals.append(peak_eval(stack, 0))
    return np.argsort(evals)


def post_evaluation(
    aligned_stacks: List[np.ndarray],
    transformations: List[List[Homography]],
):
    """
    Evaluation of the stack after alignment based on the mse error and the smoothness of the transformations

    param aligned_stacks: list of stacks after alignment
    param transformations: list of list of calculated transformations
    param a: the ratio between the two evaluations: total_eval = mse_eval + smoothness_eval

    returns: ranking of presumably best alignments in descending order
    """
    errors = list()
    for aligned_stack, transformation in zip(aligned_stacks, transformations):
        err1 = mse_eval(aligned_stack, 0)
        err2 = smoothness_eval(transformation, aligned_stack[0].shape)
        errors.append(err1 + err2)

    return np.argsort(errors)
