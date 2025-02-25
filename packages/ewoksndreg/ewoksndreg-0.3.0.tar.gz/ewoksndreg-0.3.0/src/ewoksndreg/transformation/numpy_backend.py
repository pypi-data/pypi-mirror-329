import itertools
from typing import Sequence, Optional, Tuple, Dict
import numpy

from .base import Transformation
from .homography import Homography


__all__ = ["NumpyHomography"]


class NumpyHomography(
    Homography, registry_id=Homography.RegistryId("Homography", "Numpy")
):
    def __init__(self, *args, warp_options: Optional[Dict] = None, **kw) -> None:
        if warp_options is None:
            warp_options = dict()
        self._warp_options = warp_options
        super().__init__(*args, **kw)

    def apply_coordinates(self, coord: Sequence[numpy.ndarray]) -> numpy.ndarray:
        """
        :param coord: shape `(N, M)`
        :returns: shape `(N, M)`
        """
        return homography_transform_coordinates(self.active, coord)

    def apply_data(
        self,
        data: numpy.ndarray,
        offset: Optional[numpy.ndarray] = None,
        shape: Optional[numpy.ndarray] = None,
        cval=numpy.nan,
        interpolation_order: int = 1,
    ) -> numpy.ndarray:
        """
        :param data: shape `(N1, N2, ..., M1, M2, ...)` with `len((N1, N2, ...)) = N`
        :param offset: shape `(N,)`
        :param shape: shape `(N,) = [N1', N2', ...]`
        :param cval: missing value
        :param interpolation_order: order of interpolation: 0 is nearest neighbor, 1 is bilinear,...
        :returns: shape `(N1', N2', ..., M1, M2, ...)`
        """
        kw = dict(self._warp_options)
        if shape is not None:
            kw["shape"] = shape
        if offset is not None:
            kw["offset"] = offset
        if cval is not None:
            kw["cval"] = cval
        return homography_transform_data(self.passive, data, **kw)

    def __mul__(self, other: Transformation):
        if isinstance(other, NumpyHomography):
            return NumpyHomography(
                other.passive @ self.passive, warp_options=self._warp_options
            )
        else:
            ValueError("Only concatenation of same types allowed")


def homography_transform_coordinates(
    active: numpy.ndarray, coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    """
    :param active: shape `(N+1, N+1)` or `(K, N+1, N+1)`
    :param coord: shape `(N, M)`
    :returns: shape `(N, M)` or `(K, N, M)`
    """
    N, M = coord.shape
    if active.ndim not in (2, 3) or active.shape[-2:] != (N + 1, N + 1):
        raise ValueError("matrix and coordinates dimensions do not match")
    coord = numpy.vstack(list(coord) + [numpy.ones(M)])
    hcoord = active.dot(coord)
    return hcoord[..., :-1, :] / hcoord[..., -1, :]


def homography_transform_bounding_box(
    active: numpy.ndarray, shape: Tuple[int]
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Calculate the bounding box after transforming an image with shape `shape`.
    Returns the minimum and maximum coordinates of the bounding box.

    :param active: shape `(N+1, N+1)` or `(K, N+1, N+1)`
    :param shape: shape `(N,)`
    :returns: 2-tuple of arrays with shape `(N,)` or `(K, N)`
    """
    from_bounding_box = numpy.array(list(itertools.product(*[[0, n] for n in shape]))).T
    to_bounding_box = homography_transform_coordinates(active, from_bounding_box)
    return to_bounding_box.min(axis=-1), to_bounding_box.max(axis=-1)


def homography_transform_data(
    passive: numpy.ndarray,
    data: numpy.ndarray,
    offset: Optional[numpy.ndarray] = None,
    shape: Optional[numpy.ndarray] = None,
    cval=numpy.nan,
) -> numpy.ndarray:
    """The `offset` and `shape` determine the coordinates in the output frame
    at which to interpolate the data. By default these are the coordinates of
    the `data` in the input frame (i.e. the pixel indices).

    Only nearest-neighbor interpolation is supported.

    :param passive: shape `(N+1, N+1)`
    :param data: shape `(N1, N2, ..., M1, M2, ...)` with `len((N1, N2, ...)) = N`
    :param offset: shape `(N,)`
    :param shape: shape `(N,) = [N1', N2', ...]`
    :param cval: missing value
    :returns: shape `(N1', N2', ..., M1, M2, ...)`
    """
    N = passive.shape[0] - 1
    if passive.shape != (N + 1, N + 1):
        raise ValueError("requires a square matrix")
    if data.ndim < N:
        raise ValueError("passive and data dimensions do not match")

    if offset is not None:
        offset = numpy.asarray(offset)
        if offset.shape != (N,):
            raise ValueError("passive and offset dimensions do not match")
        passive = passive.copy()
        passive[:N, N] = offset

    shape_data = numpy.asarray(data.shape[:N])
    if shape is None:
        shape_out = shape_data.copy()
    else:
        shape_out = numpy.asarray(shape)
        if shape_out.shape != (N,):
            raise ValueError("passive and shape dimensions do not match")

    # Output coordinates
    xout = [numpy.arange(n, dtype=int) for n in shape_out]
    xout = numpy.meshgrid(*xout, indexing="ij")
    xout = numpy.array([x.flatten() for x in xout])  # (N, M) with M=N1*N2*...

    # Corresponding input coordinates
    xdata = numpy.round(homography_transform_coordinates(passive, xout)).astype(int)
    valid = (xdata >= 0) & (xdata < shape_data[:, None])
    valid = numpy.bitwise_and.reduce(valid, axis=0)

    # Nearest-neighbor interpolation
    out = numpy.full(shape_out, cval, dtype=data.dtype)
    if valid.size == 0:
        return out
    out[tuple(xout[:, valid])] = data[tuple(xdata[:, valid])]
    return out
