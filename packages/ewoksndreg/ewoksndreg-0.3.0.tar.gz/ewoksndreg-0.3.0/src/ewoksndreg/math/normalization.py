import numpy as np
from typing import List, Union


def range_normalization(image: Union[np.ndarray, List]):
    """
    Scale image intensities to fit in the range [0,1]
    """
    image = np.asarray(image)
    return (image - image.min()) / (image.max() - image.min())


def stack_range_normalization(imagestack: np.ndarray):
    return np.stack([range_normalization(image) for image in imagestack])
