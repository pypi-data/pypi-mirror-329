from typing import Optional, Tuple, Sequence
import numpy

from enum import Enum


class fftConvention(str, Enum):
    numpy = "numpy"
    idl = "idl"


FFT_FREQ_CONVENTION = fftConvention.numpy
# n: number of data points in real space
# d: pixel spacing in real space
#    Convention numpy:
#     frequency = [0,...,k,-k-1,...-1]/(n.d)  (n is even, k = n/2-1  , -k-1 = -n//2, nfreq = k+1 + k+1 = n )
#                 [0,...,k,-k,...,-1]/(n.d)   (n is odd,  k = (n-1)/2, -k   = -n//2, nfreq = k+1 + k = n )
#                 k = (n+1)//2-1
#
#    Convention IDL:
#     frequency = [0,...,k,-k+1,...-1]/(n.d)  (n is even, k = n/2    , -k+1 = -n//2+1, nfreq = k+1 + k-1 = n )
#                 [0,...,k,-k,...,-1]/(n.d)   (n is odd,  k = (n-1)/2, -k   = -n//2  , nfreq = k+1 + k = n )
#                 k = (n+1)//2-(n mod 2)

FFT_NORM_CONVENTION = fftConvention.numpy
# n: number of data points in real space
# Convention numpy:
#   FT  = sum(exp(-2.pi.i.u.x))
#   IFT = sum(exp(2.pi.i.u.x))/n
# Convention IDL ():
#   FT  = sum(exp(-2.pi.i.u.x))/n
#   IFT = sum(exp(2.pi.i.u.x))


def fft_freqind(
    n: int, freqconvention: fftConvention = FFT_FREQ_CONVENTION
) -> Tuple[int, int]:
    """Calculate frequency range of an fft (multiplied by n.d)

    :param n: number of data points in real space
    :param freqconvention: even frequency convention
    """
    # frequencies = [0,...,imax,imin,...,-1]/(n.d)
    if freqconvention == fftConvention.idl:
        imin = -(n // 2) + (1 - (n % 2))
        imax = (n + 1) // 2 - (n % 2)
    else:
        imin = -(n // 2)
        imax = (n + 1) // 2 - 1
    return imin, imax


def fftfreq(
    n: int,
    d: float = 1,
    centered: bool = False,
    freqconvention: fftConvention = FFT_FREQ_CONVENTION,
) -> numpy.ndarray:
    """Fourier space with zero frequency first

    :param n: number of real space data points
    :param d: real space data point spacing
    :param centered: zero frequency in the middle
    :param freqconvention: even frequency convention
    """
    imin, imax = fft_freqind(n, freqconvention=freqconvention)
    if centered:
        freq = numpy.arange(imin, imax + 1, dtype=int)
    else:
        freq = numpy.empty(n, dtype=int)
        numpyos = imax + 1
        freq[:numpyos] = numpy.arange(numpyos, dtype=int)
        freq[numpyos:] = numpy.arange(imin, 0, dtype=int)
    return freq / float(n * d)


def fftshift(
    sigft: numpy.array, freqconvention: fftConvention = FFT_FREQ_CONVENTION
) -> numpy.ndarray:
    """Shift zero frequency to the middle

    :param sigft: signal in Fourier space
    :param freqconvention: even frequency convention
    """
    dim = numpy.array(sigft.shape)
    _, imax = fft_freqind(dim, freqconvention=freqconvention)
    numpyos = imax + 1
    out = sigft.copy()
    for k in range(len(dim)):
        ind = numpy.empty(dim[k], int)
        off = dim[k] - numpyos[k]
        ind[:off] = numpy.arange(numpyos[k], dim[k], dtype=int)
        ind[off:] = numpy.arange(numpyos[k], dtype=int)
        out = numpy.take(out, ind, axis=k)
    return out


def ifftshift(
    sigft: numpy.array, freqconvention: fftConvention = FFT_FREQ_CONVENTION
) -> numpy.ndarray:
    """Shift zero frequency to zero

    :param sigft: signal in Fourier space
    :param freqconvention: even frequency convention
    """
    dim = numpy.array(sigft.shape)
    imin, _ = fft_freqind(dim, freqconvention=freqconvention)
    numpyos = -imin
    out = sigft.copy()
    for k in range(len(dim)):
        ind = numpy.empty(dim[k], int)
        off = dim[k] - numpyos[k]
        ind[:off] = numpy.arange(numpyos[k], dim[k], dtype=int)
        ind[off:] = numpy.arange(numpyos[k], dtype=int)
        out = numpy.take(out, ind, axis=k)
    return out


def _dft1(
    arr,
    dx: float = 1,
    x0: int = 0,
    x1: Optional[int] = None,
    u: Sequence = tuple(),
    centered: bool = False,
    inverse: bool = False,
    normconvention: fftConvention = FFT_NORM_CONVENTION,
    cval=numpy.nan,
) -> numpy.ndarray:
    """Fourier transform with fixed frequencies

    :param arr: array in real or Fourier space
    :param dx: real space data point spacing
    :param x0: real space start index
    :param x1: real space end index
    :param u: Fourier space
    :param centered: zero frequency in the middle
    :param inverse: inverse Fourier transform
    :param normconvention: fft normalization
    :param cval: invalid pixel value
    """
    arr = _cval_to_zero(arr, cval)
    if dx == 1 and x0 == 0 and x1 is None and len(u) == 0 and not centered:
        if inverse:
            ret = numpy.fft.ifft(arr)
            if normconvention == fftConvention.idl:
                ret *= len(arr)
        else:
            ret = numpy.fft.fft(arr)
            if normconvention == fftConvention.idl:
                ret /= len(arr)
    else:
        # Real space
        if x1 is None:
            x1 = len(arr) - 1
        x = numpy.arange(x0, x1 + 1) * dx

        # Fourier space
        if len(u) == 0:
            u = fftfreq(len(arr), dx, centered=centered)

        # Check dimensions
        if inverse:
            if len(u) != len(arr):
                raise ValueError(
                    "Number of frequencies should be equal to the number of data points in Fourier space"
                )
            c = 2j * numpy.pi
            ret = numpy.exp(c * numpy.outer(x, u)).dot(arr)  # nx x nu x nu
        else:
            if len(x) != len(arr):
                raise ValueError(
                    "Number of times should be equal to the number of data points in real space"
                )
            c = -2j * numpy.pi
            ret = numpy.exp(c * numpy.outer(u, x)).dot(arr)  # nu x nx x nx

        # Normalization:
        if (normconvention == fftConvention.idl) ^ inverse:
            ret /= len(u)

    return ret


def _dft2(
    arr: numpy.ndarray,
    dx: float = 1,
    x0: int = 0,
    x1: Optional[float] = None,
    u: Sequence = tuple(),
    dy: float = 1,
    y0: float = 0,
    y1: Optional[float] = None,
    v: Sequence = tuple(),
    centered: bool = False,
    inverse: bool = False,
    normconvention: fftConvention = FFT_NORM_CONVENTION,
    cval=numpy.nan,
) -> numpy.ndarray:
    """Fourier transform with fixed frequencies

    Sub-region inverse Fourier transform with subpixel interpolation using the matrix for of the 2D-DFT
        Manuel Guizar-Sicairos, Samuel T. Thurman, and James R. Fienup,
        "Efficient subpixel image registration algorithms,"
        Optics Letters 33, 156-158 (2008).

    :param arr: array in real or Fourier space
    :param dx: real space data point spacing
    :param x0: real space start index
    :param x1: real space end index
    :param u: Fourier space
    :param dy: real space data point spacing
    :param y0: real space start index
    :param y1: real space end index
    :param v: Fourier space
    :param centered: zero frequency in the middle
    :param inverse: inverse Fourier transform
    :param normconvention: fft normalization
    :param cval: invalid pixel value
    """
    arr = _cval_to_zero(arr, cval)
    if (
        dx == 1
        and x0 == 0
        and x1 is None
        and len(u) == 0
        and dy == 1
        and y0 == 0
        and y1 is None
        and len(v) == 0
        and not centered
    ):
        if inverse:
            ret = numpy.fft.ifft2(arr)
            if normconvention == fftConvention.idl:
                ret *= arr.shape[0] * arr.shape[1]
        else:
            ret = numpy.fft.fft2(arr)
            if normconvention == fftConvention.idl:
                ret /= arr.shape[0] * arr.shape[1]
    else:
        # Real space
        if x1 is None:
            x1 = arr.shape[1] - 1
        if y1 is None:
            y1 = arr.shape[0] - 1
        x = numpy.arange(x0, x1 + 1) * dx
        y = numpy.arange(y0, y1 + 1) * dy

        # Fourier space
        if len(u) == 0:
            u = fftfreq(arr.shape[1], dx, centered=centered)
        if len(v) == 0:
            v = fftfreq(arr.shape[0], dy, centered=centered)

        # DFT (forward or backward)
        if inverse:
            if len(u) != arr.shape[1] or len(v) != arr.shape[0]:
                raise ValueError(
                    "Number of frequencies should be equal to the number of data points in Fourier space"
                )
            c = 2j * numpy.pi
            col_kernel = numpy.exp(c * u[:, None].dot(x[None, :]))  # nu x nx
            row_kernel = numpy.exp(c * y[:, None].dot(v[None, :]))  # ny x nv
            # ny x nv . nv x nu . nu x nx
        else:
            if len(x) != arr.shape[1] or len(y) != arr.shape[0]:
                raise ValueError(
                    "Number of times should be equal to the number of data points in Fourier space"
                )
            c = -2j * numpy.pi
            col_kernel = numpy.exp(c * x[:, None].dot(u[None, :]))  # nx x nu
            row_kernel = numpy.exp(c * v[:, None].dot(y[None, :]))  # nv x ny
            # nv x ny . ny x nx . nx x nu
        ret = row_kernel.dot(arr).dot(col_kernel)

        # Normalization:
        if (normconvention == fftConvention.idl) ^ inverse:
            ret /= len(u) * len(v)

    return ret


def fft1(arr: numpy.ndarray, **kwargs) -> numpy.ndarray:
    """Fourier transform with default frequencies

    :param arr: array in real space
    :returns: array in fourier space
    """
    return _dft1(arr, inverse=False, **kwargs)


def fft2(arr: numpy.ndarray, **kwargs) -> numpy.ndarray:
    """Fourier transform with default frequencies

    :param arr: array in real space
    :returns: array in fourier space
    """
    return _dft2(arr, inverse=False, **kwargs)


def fft(arr: numpy.ndarray, **kwargs) -> numpy.ndarray:
    """Fourier transform with default frequencies

    :param arr: array in real space
    :returns: array in fourier space
    """
    if arr.size in arr.shape:
        if arr.ndim > 1:
            arr = arr.flatten()
        return _dft1(arr, inverse=False, **kwargs)
    else:
        return _dft2(arr, inverse=False, **kwargs)


def ifft1(arr: numpy.ndarray, **kwargs) -> numpy.ndarray:
    """Inverse Fourier transform with default frequencies

    :param arr: array in Fourier space
    :returns: array in fourier space
    """
    return _dft1(arr, inverse=True, **kwargs)


def ifft2(arr: numpy.ndarray, **kwargs) -> numpy.ndarray:
    """Inverse Fourier transform with default frequencies

    :param arr: array in real space
    :returns: array in fourier space
    """
    return _dft2(arr, inverse=True, **kwargs)


def ifft(arr: numpy.ndarray, **kwargs) -> numpy.ndarray:
    """Inverse Fourier transform with default frequencies

    :param arr: array in real space
    :returns: array in fourier space
    """
    if arr.size in arr.shape:
        if arr.ndim > 1:
            arr = arr.flatten()
        return _dft1(arr, inverse=True, **kwargs)
    else:
        return _dft2(arr, inverse=True, **kwargs)


def _cval_to_zero(img: numpy.ndarray, cval):
    if cval != 0:
        if numpy.isnan(cval):
            missing = numpy.isnan(img)
        else:
            missing = img == cval
        bmissing = numpy.any(missing)
    else:
        bmissing = False

    if bmissing:
        img = img.copy()
        img[missing] = 0
    return img


def ifft_interpolate(
    arr: numpy.ndarray,
    ROIoffset: Sequence,
    ROIsize: Sequence,
    sampling: int = 1,
    cval=numpy.nan,
) -> numpy.ndarray:
    """Interpolate array in fourier space

    Sub-region inverse Fourier transform with subpixel interpolation
        Manuel Guizar-Sicairos, Samuel T. Thurman, and James R. Fienup,
        "Efficient subpixel image registration algorithms,"
        Optics Letters 33, 156-158 (2008).

    :param arr: array in fourier space
    :param ROIoffset: sub-pixel grid (super-space)
    :param ROIsize: sub-pixel grid (super-space)
    :returns: inverse FFT on sub-pixel grid
    """
    if arr.size in arr.shape:
        # Super space
        x0 = -ROIoffset
        x1 = x0 + ROIsize - 1

        # Frequencies corresponding to super space
        nu = arr.size
        u = fftfreq(nu, d=sampling)

        return ifft1(arr, x0=x0, x1=x1, u=u, cval=cval)
    else:
        # Super space
        x0 = -ROIoffset[1]
        x1 = x0 + ROIsize[1] - 1
        y0 = -ROIoffset[0]
        y1 = y0 + ROIsize[0] - 1

        # Frequencies corresponding to super space
        nu = arr.shape[1]
        nv = arr.shape[0]
        u = fftfreq(nu, d=sampling)
        v = fftfreq(nv, d=sampling)

        return ifft2(arr, x0=x0, x1=x1, u=u, y0=y0, y1=y1, v=v, cval=cval)
