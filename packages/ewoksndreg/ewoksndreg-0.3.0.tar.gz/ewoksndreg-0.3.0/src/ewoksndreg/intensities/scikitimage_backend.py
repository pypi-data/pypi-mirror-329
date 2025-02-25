import numpy
from typing import Optional
from .base import IntensityMapping
from ..transformation.types import TransformationType
from ..transformation.scikitimage_backend import SciKitImageHomography
from ..math.fft import fft2, fftshift

from packaging.version import Version
import skimage
from skimage.transform import warp_polar, SimilarityTransform
from skimage.registration import phase_cross_correlation as _phase_cross_correlation


def phase_cross_correlation(img1, img2, **kw) -> numpy.ndarray:
    version = Version(skimage.__version__)

    if version >= Version("0.21.0"):
        shift, _, _ = _phase_cross_correlation(img1, img2, **kw)
        return shift
    return _phase_cross_correlation(
        img1, img2, return_error=False, **kw  # deprecated in 0.21 and removed in 0.22
    )


class SkimageCorrelationIntensityMapping(
    IntensityMapping,
    registry_id=IntensityMapping.RegistryId("CrossCorrelation", "SciKitImage"),
):
    SUPPORTED_TRANSFORMATIONS = ["translation"]

    def __init__(
        self,
        transfo_type: TransformationType,
        upsample_factor: int = 5,
        normalization: bool = True,
        mask: Optional[numpy.ndarray] = None,
        **kw,
    ) -> None:
        self._factor = upsample_factor
        if normalization:
            self._normalization = "phase"
        else:
            self._normalization = None
        self._mask = mask
        super().__init__(transfo_type, **kw)

    def identity(self, dimension: int = 2) -> SciKitImageHomography:
        return SciKitImageHomography(
            numpy.identity(dimension + 1), TransformationType.identity
        )

    def calculate(
        self,
        from_image: numpy.ndarray,
        to_image: numpy.ndarray,
    ) -> SciKitImageHomography:
        if self.type == self.type.translation:
            if self._mask is not None and numpy.any(self._mask):
                self._mask = self._mask.astype(bool)
                shift = phase_cross_correlation(
                    from_image,
                    to_image,
                    moving_mask=self._mask,
                    reference_mask=self._mask,
                )
            else:
                shift = phase_cross_correlation(
                    from_image,
                    to_image,
                    normalization=self._normalization,
                    upsample_factor=self._factor,
                )

            passive = numpy.identity(from_image.ndim + 1)
            passive[0:-1, -1] = shift
            return SciKitImageHomography(passive, transfo_type="translation")
        elif self.type == self.type.similarity:
            # magnitude of FFT
            from_ft = numpy.abs(fftshift(fft2(from_image)))
            to_ft = numpy.abs(fftshift(fft2(to_image)))

            # transform magnitudes into log-polar
            radius = min(from_image.shape) // 4
            warped_from_ft = warp_polar(from_ft, radius=radius, scaling="log", order=1)
            warped_to_ft = warp_polar(to_ft, radius=radius, scaling="log", order=1)

            # half the log-polar fourier magnitudes and calculate their relative shift
            warped_from_ft = warped_from_ft[: warped_from_ft.shape[0] // 2, :]
            warped_to_ft = warped_to_ft[: warped_to_ft.shape[0] // 2, :]
            shifts = phase_cross_correlation(
                warped_from_ft,
                warped_to_ft,
                normalization=self._normalization,
                upsample_factor=self._factor,
            )

            # recover scale and angle from the shift
            recovered_angle = shifts[0] / 180 * numpy.pi
            scale = numpy.exp(-shifts[1] * numpy.log(radius) / radius)

            # apply scale and angle as a centered transform
            similarity = SimilarityTransform(scale=scale, rotation=-recovered_angle)
            translation = SimilarityTransform(
                translation=(from_image.shape[0] / 2, from_image.shape[1] / 2)
            )
            mtranslation = SimilarityTransform(
                translation=(-from_image.shape[0] / 2, -from_image.shape[1] / 2)
            )
            full = mtranslation + similarity + translation
            return SciKitImageHomography(full.params, transfo_type="similarity")

        else:
            raise ValueError(
                "Only translation possible with SciKitImage Phase Correlation"
            )
