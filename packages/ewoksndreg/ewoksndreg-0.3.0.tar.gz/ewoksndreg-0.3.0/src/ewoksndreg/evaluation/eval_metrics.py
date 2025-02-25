import numpy as np
from skimage.filters import gaussian
from typing import Sequence, Tuple
from ..transformation.homography import Homography
from ..math.normalization import range_normalization


def noisy_eval(stack: np.ndarray) -> float:
    """
    Determines how noisy the images in the given stack are
    This is determined by denoising the image with a gaussian filter and comparing the variance before and after.
    Return value is big if the denoising decreased the variance a lot.

    param stack: array of shape [N,H,W]
    """
    total = 0
    for image in stack:
        image = range_normalization(image)
        var = image.var()
        newvar = gaussian(image).var()
        total += var / newvar
    return total / len(stack)


def peak_eval(stack: np.ndarray, reference: int) -> float:
    """
    Calculate a measure of how reliable a stack of images is to determine the transformations between the images.

    The measure is based on phase cross correlation which generates an image with the peak with coordinates corresponding to the shift.
    This eval calculates how distinguished this peak is by comparing it to the mean of the phase correlation image

    param stack: the aligned or unaligned stack with pixel values in [0,1]
    """
    total = 0
    ref = np.fft.fft2(stack[reference])
    for image in stack:
        transform = np.fft.fft2(image)
        prod = ref * transform.conj()
        peak = np.abs(np.fft.ifft2(prod / np.abs(prod)))
        total += peak.mean() - peak.max()
    return total / len(stack)


def mse_eval(stack: np.ndarray, reference: int) -> float:
    """
    Evaluate success based on the remaining mse error after alignment

    param stack: Aligned stack of images with pixel values in [0,1]
    """
    total = 0
    for image in stack:
        total += np.nanmean((stack[reference] - image) ** 2)
    return total / len(stack)


def smoothness_eval(
    transformations: Sequence[Homography], img_size: Tuple[int, ...]
) -> float:
    """
    Evaluates the transformations by smoothness.

    This is done by transforming the coordinates of the corners of the image and looking at how much these change by successive transformations

    param transformations: Sequence of Homographies
    param img_size: Shape of the images that these transformations are meant for
    """
    i, j = img_size
    points = np.array([[0, 0, i, i], [0, j, 0, j]])
    corners_after = [transfo.apply_coordinates(points) for transfo in transformations]
    corners_diff = [
        (corners_after[i] - corners_after[i - 1]) for i in range(1, len(corners_after))
    ]
    size = np.array([[i], [j]])
    corners_diff = [c / size for c in corners_diff]
    corners_diff = np.linalg.norm(corners_diff, axis=1)
    return np.mean(corners_diff)
