import numpy
from .base import IntensityMapping
from ..math import center
from ..math import fft
from ..transformation import TransformationType
from ..transformation.numpy_backend import NumpyHomography

__all__ = ["NumpyCrossCorrelationIntensityMapping"]


class NumpyCrossCorrelationIntensityMapping(
    IntensityMapping,
    registry_id=IntensityMapping.RegistryId("CrossCorrelation", "Numpy"),
):
    SUPPORTED_TRANSFORMATIONS = ["translation"]

    def __init__(self, transfo_type: TransformationType, **kw) -> None:
        self._to_image_ft = None
        super().__init__(transfo_type, **kw)

    def calculate(
        self, from_image: numpy.ndarray, to_image: numpy.ndarray
    ) -> NumpyHomography:
        from_image_ft = fft.fft2(from_image)
        if to_image is not self._to_image_ft:
            self._to_image_fft = fft.fft2(to_image)
        passive = numpy.identity(3)
        passive[0:2, 2] = determine_shift(from_image_ft, self._to_image_fft)
        return NumpyHomography(passive, self._type)

    def identity(self, dimension: int = 2) -> NumpyHomography:
        return NumpyHomography(
            numpy.identity(dimension + 1), TransformationType.identity
        )


def determine_shift(
    img1ft: numpy.ndarray,
    img2ft: numpy.ndarray,
    sampling: int = 1,
    maxmethod: str = "max",
):
    """Determine shift between images using their Fourier transforms"""
    is1D = img1ft.size in img1ft.shape

    # Calculate shift without subpixel precision
    # Ideally this should be a delta function: real(F.G*/(|F|.|G|))
    # In reality this doesn't seem to work, somehow |F.G*| is better, no idea why
    image_product = img1ft * img2ft.conj()
    # image_product /= ftmodulus(image_product)
    cross_correlation = fft.ifft(image_product)
    shift = cc_maximum(cross_correlation)

    # Shift indices = [0,...,imax,imin,...,-1]
    if is1D:
        _, imax = fft.fft_freqind(cross_correlation.size)
        if shift > imax:
            shift -= cross_correlation.size
    else:
        s = numpy.array(cross_correlation.shape)
        _, imax = fft.fft_freqind(s)
        shift[shift > imax] -= s[shift > imax]

    if sampling <= 1:
        return shift

    # Calculate shift with subpixel precision by interpolating
    # the cross-correlation around the maximum (or center-of-mass).

    # real-space: n, d=1, shift=s
    # super-space: n*sampling, d=1, shift=s*sampling
    if is1D:
        ROIsize = 4 * sampling
    else:
        # ROI in super-space = 3x3 pixels in real-space
        ROIsize = sampling * numpy.array((3, 3))
    _, ksampled = fft.fft_freqind(ROIsize)  # ROI center

    # ROI = [0,1,...,ROIsize-1] - ksampled + shift*sampling  (so that maximum in the middle)
    ROIoffset = ksampled - shift * sampling
    cross_correlation = fft.ifft_interpolate(image_product, ROIoffset, ROIsize)
    # cross_correlation /= img2ft.shape[0]*img2ft.shape[1] * self.sampling ** 2

    # Get fit, maximum, centroid, ...
    shiftsampled = cc_maximum(cross_correlation, maxmethod=maxmethod)

    # Shift from super space to real space
    shift = (shiftsampled - ROIoffset) / sampling

    return shift


def cc_maximum(cross_correlation: numpy.ndarray, maxmethod: str = "max"):
    data = ftmodulus(cross_correlation)
    # data = cross_correlation.real

    if maxmethod == "centroid":
        shift = center.fcentroid(data)
    elif maxmethod == "fit":
        shift = center.fgaussmax(data)
    else:
        shift = center.fmax(data)

    return shift


def ftmodulus(imgft: numpy.ndarray) -> numpy.ndarray:
    imgabs = numpy.abs(imgft)
    imgabs[imgabs < 1.0e-20] = 1
    return imgabs
