import numpy as np

from typing import List, Tuple


def crop_stack(stack: np.ndarray) -> np.ndarray:
    """
    Crops the images to exclude all NaN values. Only works for translated images

    param stack: Stack of translated images of form [N,H,W] with nan values in the empty sections

    returns: Stack of cropped images of form [N, H', W']
    """
    boolean = np.isnan(stack)
    full_pixels = boolean.sum(axis=0) == 0
    indices = np.nonzero(full_pixels)
    new_shape = tuple([index.max() - index.min() + 1 for index in indices])
    return stack[:, full_pixels].reshape((-1, *new_shape))


def crop_edges(stack: np.ndarray) -> Tuple[slice, slice]:
    """
    Calculates the slices such that they correspond to cropping out NaN values

    param stack: Stack of translated images of form [N,H,W] with nan values in the empty sections

    returns: two slices which crop the individual images to remove nan values
    """
    boolean = np.isnan(stack)
    full_pixels = boolean.sum(axis=0) == 0
    indices = np.nonzero(full_pixels)
    edges = [slice(index.min(), index.max() + 1) for index in indices]
    return edges


def calc_NaN_edges(image: np.ndarray) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Calculates the biggest subimage that doesn't contain NaN-values
    Usable for situations where loading the entire stack is not feasible
    ----
    param image: Translated image with potential NaN values on the edges

    returns: two tuples containing the 4 borders of the image: ((top,left), (bottom,right))
    """

    boolean = np.isnan(image) == 0
    xindex, yindex = np.nonzero(boolean)
    return (xindex.min(), yindex.min()), (xindex.max() + 1, yindex.max() + 1)


def crop_translations(
    transformations: List,
    include: List[int],
    img_size: Tuple,
    interpolation_order: int = 1,
):
    """
    Calculate the area of the images which doesn't include any NaN values based on the calculated transformations

    param transformations: list of translations
    param include: list of indices of the transformations which should be considered for cropping
    param img_size: image size of the images that will be cropped
    param interpolation_order: The order of the polynomials that will be used to resample the image, as higher orders create more NaN values

    returns: two slices which crop the individual images to remove nan values
    """
    order = interpolation_order
    xshift = [
        int(hom.passive[0, 2]) for i, hom in enumerate(transformations) if i in include
    ]
    yshift = [
        int(hom.passive[1, 2]) for i, hom in enumerate(transformations) if i in include
    ]
    x0, x1 = order, img_size[0] - order
    y0, y1 = order, img_size[1] - order
    if min(xshift) < 0:
        x0 += -min(xshift) + 1
    if max(xshift) > 0:
        x1 -= max(xshift) + 1
    x = slice(x0, x1)

    if min(yshift) < 0:
        y0 += -min(yshift)
    if max(yshift) > 0:
        y1 -= max(yshift)
    y = slice(y0, y1)
    return (x, y)
