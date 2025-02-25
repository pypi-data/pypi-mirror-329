import numpy as np
import pytest

from ..evaluation.eval_metrics import noisy_eval, peak_eval, smoothness_eval
from .data.data_for_registration import images
from ..math.normalization import stack_range_normalization
from ..transformation.numpy_backend import NumpyHomography
from ..transformation.homography import matrix_from_params


@pytest.mark.parametrize("image", argvalues=["astronaut", "gravel", "cell"])
@pytest.mark.parametrize("noise", ["uniform", "gaussian"])
def test_noisy_metric(image, noise):
    imagestack, active, passive = images("rigid", nimages=5, name=image)
    imagestack = np.stack(imagestack)
    if noise == "uniform":
        noise = np.random.random(imagestack.shape)
    elif noise == "gaussian":
        noise = np.random.normal(size=(imagestack.shape))
    stacks = [imagestack + noise * i * 0.1 for i in range(5)]
    stacks = [stack_range_normalization(stack) for stack in stacks]
    errors = [noisy_eval(stack) for stack in stacks]
    for i in range(len(errors) - 1):
        assert errors[i] < errors[i + 1] + 0.1


@pytest.mark.parametrize("image", argvalues=["astronaut", "gravel", "cell"])
@pytest.mark.parametrize("noise", ["uniform", "gaussian"])
def test_peak_metric(image, noise):
    imagestack, active, passive = images("translation", nimages=5, name=image)
    imagestack = np.stack(imagestack)
    if noise == "uniform":
        noise = np.random.random(imagestack.shape)
    elif noise == "gaussian":
        noise = np.random.normal(size=(imagestack.shape))

    stacks = [imagestack + noise * i * 0.05 for i in range(5)]
    stacks = [stack_range_normalization(stack) for stack in stacks]
    errors = [peak_eval(stack, 0) for stack in stacks]
    for i in range(len(errors) - 1):
        assert errors[i] < errors[i + 1] + 0.01


def test_smoothness_metric():
    img_size = (120, 120)
    matrices = [
        np.array([[1, 0, i], [0, 1, i], [0, 0, 1]], dtype=np.float64) for i in range(10)
    ]
    transformations = [NumpyHomography(matrix) for matrix in matrices]
    bigger_matrices = [
        np.array([[1, 0, 2 * i], [0, 1, 2 * i], [0, 0, 1]], dtype=np.float64)
        for i in range(10)
    ]
    bigger_transformations = [NumpyHomography(matrix) for matrix in bigger_matrices]
    matrices = [
        np.array([[1, 0, i * ((-1) ** i)], [0, 1, i], [0, 0, 1]], dtype=np.float64)
        for i in range(10)
    ]
    jagged_transformations = [NumpyHomography(matrix) for matrix in matrices]
    val1 = smoothness_eval(transformations, img_size)
    val2 = smoothness_eval(bigger_transformations, img_size)
    val3 = smoothness_eval(jagged_transformations, img_size)
    print(val1, val2, val3)
    assert val1 < val2 and val2 < val3


def test_smoothness_metric_rot():
    img_size = (120, 120)
    matrices = [matrix_from_params([i / 20, 0, 0], "rigid") for i in range(10)]
    transformations = [NumpyHomography(matrix) for matrix in matrices]
    bigger_matrices = [matrix_from_params([i / 10, 0, 0], "rigid") for i in range(10)]
    bigger_transformations = [NumpyHomography(matrix) for matrix in bigger_matrices]
    val1 = smoothness_eval(transformations, img_size)
    val2 = smoothness_eval(bigger_transformations, img_size)
    assert val1 < val2


def test_smoothness_metric_size():
    img_size = (50, 50)
    img_size2 = (100, 100)
    matrices = [matrix_from_params([0, i, i], "rigid") for i in range(10)]
    transformations = [NumpyHomography(matrix) for matrix in matrices]
    val1 = smoothness_eval(transformations, img_size)
    val2 = smoothness_eval(transformations, img_size2)
    assert val1 > val2
