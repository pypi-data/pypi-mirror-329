import numpy as np
from typing import Optional
from skimage.filters import (
    window,
    difference_of_gaussians,
    sobel,
    gaussian,
    sato,
    meijering,
    median,
)

from enum import Enum


class WindowType(str, Enum):
    boxcar = "boxcar"
    triang = "triang"
    blackman = "blackman"
    hamming = "hamming"
    hann = "hann"
    bartlett = "bartlett"
    flattop = "flattop"
    parzen = "parzen"
    bohman = "bohman"
    blackmanharris = "blackmanharris"
    nuttall = "nuttall"
    barthann = "barthann"
    cosine = "cosine"
    exponential = "exponential"
    tukey = "tukey"
    taylor = "taylor"
    lanczos = "lanczos"


class FilterType(str, Enum):
    gaussian = "gaussian"
    median = "median"
    sobel = "sobel"
    sato = "sato"
    meijering = "meijering"


def preprocess(
    image: np.ndarray,
    apply_filter: Optional[FilterType] = None,
    filter_parameter: float = 1,
    apply_low_pass: float = 0.0,
    apply_high_pass: float = 0.0,
    apply_window: Optional[WindowType] = None,
    pin_range: bool = False,
):
    if filter_parameter == 0:
        filter_parameter = 1
    if apply_filter == "gaussian":
        image = gaussian(image, filter_parameter)
    if apply_filter == "median":
        image = median(image, np.full((3, 3), 1))
    elif apply_filter == "sobel":
        image = sobel(image)
    elif apply_filter == "sato":
        image = sato(image, np.arange(1, filter_parameter * 2, 2))
    elif apply_filter == "meijering":
        image = meijering(image, np.arange(1, filter_parameter * 2, 2))

    if apply_low_pass > 0 and apply_high_pass > apply_low_pass:
        image = difference_of_gaussians(image, apply_low_pass, apply_high_pass)
    elif apply_low_pass > 0:
        image = difference_of_gaussians(image, apply_low_pass, max(image.shape))
    elif apply_high_pass > 0:
        image = difference_of_gaussians(image, 0, apply_high_pass)

    if pin_range:
        image = (image - image.min()) / (image.max() - image.min())

    if apply_window:
        image = image * window(apply_window, image.shape)

    return image
