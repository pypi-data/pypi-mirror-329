from typing import Optional, Sequence, Dict
import numpy

from ewoksndreg.transformation.homography import type_from_matrix, reverse_indices
from ewoksndreg.transformation.base import Transformation
from ewoksndreg.transformation.types import TransformationType
import SimpleITK as sitk

__all__ = ["SimpleITKTransformation"]


class SimpleITKTransformation(
    Transformation, registry_id=Transformation.RegistryId("Transformation", "SimpleITK")
):
    def __init__(
        self,
        transfo_type: Optional[TransformationType] = None,
        warp_options: Optional[Dict] = None,
        transformation: Optional[sitk.Transform] = None,
        passive: Optional[numpy.ndarray] = None,
        displacement_field: Optional[numpy.ndarray] = None,
        bspline: Optional[numpy.ndarray] = None,
    ) -> None:
        if warp_options is None:
            warp_options = dict()
        self._warp_options = warp_options
        self._passive = None
        if transformation:
            self._sitk_passive = transformation
            super().__init__(self.type_from_transform(transformation))

        elif displacement_field is not None:
            super().__init__("displacement_field")
            self._sitk_passive = sitk.DisplacementFieldTransform(
                sitk.GetImageFromArray(displacement_field, True)
            )

        elif bspline is not None:
            super().__init__("bspline")
            spline_order = bspline[-1]
            self._sitk_passive = sitk.BSplineTransform(bspline[:-1], spline_order)

        elif passive is not None:
            if transfo_type is None:
                transfo_type = type_from_matrix(passive)
            super().__init__(transfo_type)
            matrix = passive[:-1]

            dim = matrix.shape[0]
            if self.type == self.type.identity:
                self._sitk_passive = sitk.TranslationTransform(dim)
            elif self.type == self.type.translation:
                self._sitk_passive = sitk.TranslationTransform(dim)
                self._sitk_passive.SetOffset(matrix[:, -1][::-1])

            elif self.is_homography():
                if self.type == self.type.rigid and dim == 2:
                    self._sitk_passive = sitk.Euler2DTransform()
                elif self.type == self.type.rigid and dim == 3:
                    self._sitk_passive = sitk.Euler3DTransform()
                elif dim == 2 and (
                    self.type == self.type.similarity or self._type == self._type.rigid
                ):
                    self._sitk_passive = sitk.Similarity2DTransform()
                elif dim == 3 and (
                    self.type == self.type.similarity or self._type == self._type.rigid
                ):
                    self._sitk_passive = sitk.Similarity3DTransform()
                elif self.type == self.type.affine:
                    self._sitk_passive = sitk.AffineTransform(dim)
                self._sitk_passive.SetCenter(dim * [0])
                self._sitk_passive.SetMatrix(tuple(matrix[:, 0:-1].T.flatten()))
                self._sitk_passive.SetTranslation(tuple(matrix[:, -1][::-1]))

        try:
            self._sitk_passive
        except AttributeError:
            self._sitk_passive = self.get_identity(self.type)

    @property
    def displacement_field(self) -> numpy.ndarray:
        try:
            return sitk.GetArrayFromImage(self._sitk_passive.GetDisplacementField())
        except AttributeError:
            raise AttributeError(
                "Tried to get displacement field but transformation type is {self.type}"
            )

    @property
    def passive(self) -> numpy.ndarray:
        if self._passive is not None:
            return self._passive
        elif self.is_homography():
            return self._add_passive()
        else:
            raise AttributeError(
                "the passive matrix is only available if the transformation type can be represented by a 2x3 matrix"
            )

    def get_identity(self, transfo_type: TransformationType, dim: int = 2):
        if transfo_type == "translation":
            transform = sitk.TranslationTransform(dim)
        if transfo_type == "rigid":
            transform = sitk.Euler2DTransform() if dim == 2 else sitk.Euler3DTransform()
        if transfo_type == "similarity":
            transform = (
                sitk.Similarity2DTransform()
                if dim == 2
                else sitk.Similarity3DTransform()
            )
        if transfo_type == "affine":
            transform = sitk.AffineTransform(dim)
        if transfo_type in ["bspline", "displacement_field"]:
            raise ValueError(
                "Can't create empty displacement field without image specifications"
            )
        return transform

    def type_from_transform(self, transformation: sitk.Transform):
        if isinstance(transformation, sitk.TranslationTransform):
            transfo_type = "translation"
        elif isinstance(transformation, (sitk.Euler2DTransform, sitk.Euler3DTransform)):
            transfo_type = "rigid"
        elif isinstance(
            transformation, (sitk.Similarity2DTransform, sitk.Similarity3DTransform)
        ):
            transfo_type = "similarity"
        elif isinstance(transformation, (sitk.AffineTransform)):
            transfo_type = "affine"
        elif isinstance(transformation, sitk.DisplacementFieldTransform):
            transfo_type = "displacement_field"
        elif isinstance(transformation, sitk.BSplineTransform):
            transfo_type = "bspline"
        else:
            transfo_type = "composite"
        return transfo_type

    def _add_passive(self):
        passive = numpy.identity(3)
        if self._type == self._type.identity:
            self._passive = passive

        elif self._type == self._type.translation:
            passive[1::-1, 2] = self._sitk_passive.GetOffset()
            self._passive = passive

        elif self.is_homography():
            cx, cy = self._sitk_passive.GetCenter()
            A = self._sitk_passive.GetMatrix()
            tx, ty = self._sitk_passive.GetTranslation()
            matrix = numpy.asarray([[A[0], A[1], 0], [A[2], A[3], 0], [0, 0, 1]])
            pre = numpy.asarray([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]])
            post = numpy.asarray([[1, 0, tx + cx], [0, 1, ty + cy], [0, 0, 1]])
            passive = post @ matrix @ pre
            self._passive = reverse_indices(passive)
        return self._passive

    def apply_coordinates(self, coord: Sequence[numpy.ndarray]) -> numpy.ndarray:
        """
        :param coord: shape `(N, M)`
        :returns: shape `(N, M)`
        """
        coord = coord[::-1]
        transformed = [
            self._sitk_passive.GetInverse().TransformPoint(point.astype(numpy.float64))
            for point in numpy.transpose(coord)
        ]
        return numpy.transpose(transformed)[::-1]

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
            kw["output_shape"] = shape
        if offset is not None:
            kw["offset"] = offset
        if cval is not None:
            kw["cval"] = cval

        if interpolation_order is not None:
            order = interpolation_order
        else:
            order = 1

        image = sitk.GetImageFromArray(data)
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(image)

        if order == 0:
            resampler.SetInterpolator(sitk.sitkNearestNeighbor)
        elif order == 1:
            resampler.SetInterpolator(sitk.sitkLinear)
        elif order == 2:
            resampler.SetInterpolator(sitk.sitkBSpline1)
        elif order == 3:
            resampler.SetInterpolator(sitk.sitkBSpline2)
        elif order == 4:
            resampler.SetInterpolator(sitk.sitkBSpline3)
        else:
            raise ValueError("Only interpolation up to order 4 possible")

        resampler.SetDefaultPixelValue(kw["cval"])
        resampler.SetTransform(self._sitk_passive)

        out = resampler.Execute(image)
        return sitk.GetArrayFromImage(out)

    def __mul__(self, other: Transformation):
        if isinstance(other, SimpleITKTransformation):
            dim = self._sitk_passive.GetDimension()
            if other._sitk_passive.GetDimension() != dim:
                raise TypeError("Transformations must have same dimensions")
            if dim == 2 and self.is_homography() and other.is_homography():
                return SimpleITKTransformation(passive=other.passive @ self.passive)
            comp = sitk.CompositeTransform(dim)
            comp.AddTransform(self._sitk_passive)
            comp.AddTransform(other._sitk_passive)
            comp.FlattenTransform()
            return SimpleITKTransformation(
                transfo_type="composite",
                warp_options=self._warp_options,
                transformation=comp,
            )
        else:
            raise TypeError(
                "SimpleITK Transformation can only be concatenated with other SimpleITK Transformation"
            )
