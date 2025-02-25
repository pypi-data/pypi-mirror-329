import numpy as np

from ..math.crop import crop_edges, crop_stack


def test_crop_stack():
    array = np.zeros((15, 15, 15))
    array[:, 0:2, :] = np.nan
    cropped = crop_stack(array)
    assert cropped.shape == (15, 13, 15)
    array[10, :, 0] = np.nan
    cropped = crop_stack(array)
    assert cropped.shape == (15, 13, 14)


def test_crop_edges():
    array = np.zeros((15, 15, 15))
    array[:, 0:2, :] = np.nan
    x, y = crop_edges(array)
    assert x == slice(2, 15)
    assert y == slice(0, 15)
    array[10, :, 0] = np.nan
    x, y = crop_edges(array)
    assert x == slice(2, 15)
    assert y == slice(1, 15)
