import numpy as np
from typing import Tuple, Union


def resize(image: np.ndarray, out_shape: Tuple[int], order: int = 0) -> np.ndarray:
    if image.ndim != len(out_shape):
        raise ValueError("New shape must have same dimensionality as image")

    in_shape = image.shape

    ranges = [np.arange(0, shp, shp / out_shape[i]) for i, shp in enumerate(in_shape)]
    X = np.meshgrid(*ranges[::-1])
    X = np.array(X).astype(int)
    X = X[::-1]
    if order == 0:
        result = image[X[0], X[1]]
        result = np.reshape(result, out_shape)
        return result


def rescale(
    image: np.ndarray, factor: Union[float, int, Tuple], order: int = 0
) -> np.ndarray:
    shp = image.shape

    factor = float(factor) if isinstance(factor, int) else factor

    if isinstance(factor, float):
        factor = (factor,) * image.ndim

    if len(factor) != image.ndim:
        raise ValueError(
            f"{len(factor)} scaling factors must match image dimension {image.ndim}"
        )

    new_shape = tuple([int(x * factor[i]) for i, x in enumerate(shp)])

    return resize(image, new_shape, order=order)
