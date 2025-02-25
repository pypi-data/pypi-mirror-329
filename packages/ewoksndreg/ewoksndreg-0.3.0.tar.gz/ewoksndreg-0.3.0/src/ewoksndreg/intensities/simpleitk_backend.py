import SimpleITK as sitk
import numpy
from typing import Optional
from typing_extensions import Literal
from .base import IntensityMapping
from ..transformation.types import TransformationType
from ..transformation.simpleitk_backend import SimpleITKTransformation
from .types import SitkMetricType, SitkOptimizerType


class sitkOptimizerIntesityMapping(
    IntensityMapping,
    registry_id=IntensityMapping.RegistryId("Optimization", "SimpleITK"),
):
    SUPPORTED_TRANSFORMATIONS = [
        "translation",
        "rigid",
        "similarity",
        "affine",
        "bspline",
        "displacement_field",
    ]

    def __init__(
        self,
        transfo_type: TransformationType,
        metric: SitkMetricType = SitkMetricType.MeanSquares,
        optimizer: SitkOptimizerType = SitkOptimizerType.LBFGSB,
        order: int = 1,
        mask: Optional[numpy.ndarray] = None,
        pyramid_levels: int = 1,
        mesh_size: Optional[tuple] = None,
        sampling: Optional[Literal["random", "regular"]] = None,
        sampling_percentage: int = 0.5,
        **kw,
    ) -> None:
        self._registration_method = sitk.ImageRegistrationMethod()
        self._metric = SitkMetricType(metric)
        self._optimizer = SitkOptimizerType(optimizer)
        self._mask = mask
        self._mesh_size = mesh_size
        self._levels = pyramid_levels

        if order == 0:
            self._registration_method.SetInterpolator(sitk.sitkNearestNeighbor)
        elif order == 1:
            self._registration_method.SetInterpolator(sitk.sitkLinear)
        elif order == 2:
            self._registration_method.SetInterpolator(sitk.sitkBSpline1)
        elif order == 3:
            self._registration_method.SetInterpolator(sitk.sitkBSpline2)
        elif order == 4:
            self._registration_method.SetInterpolator(sitk.sitkBSpline3)
        elif order == 5:
            self._registration_method.SetInterpolator(sitk.sitkBSpline4)

        self._order = order

        super().__init__(transfo_type, **kw)

        # set the metric
        if self.type == self.type.displacement_field:
            self._registration_method.SetMetricAsDemons(0.00001)
        elif self._metric == self._metric.CrossCorrelation:
            self._registration_method.SetMetricAsCorrelation()
        elif self._metric == self._metric.ANTSNeighborhoodCorrelation:
            self._registration_method.SetMetricAsANTSNeighborhoodCorrelation()
        elif self._metric == self._metric.JointHistogramMutualInformation:
            self._registration_method.SetMetricAsJointHistogramMutualInformation()
        elif self._metric == self._metric.MattesMutualInformation:
            self._registration_method.SetMetricAsMattesMutualInformation()
        elif self._metric == self._metric.MeanSquares:
            self._registration_method.SetMetricAsMeanSquares()
        else:
            raise ValueError(
                f"metric {self._metric} not supported by SimpleITK, choose from {list(SitkMetricType.__members__)}"
            )

        # set the optimizer
        if self._optimizer == self._optimizer.Exhaustive:
            self._registration_method.SetOptimizerAsExhaustive((10, 10))
        elif self._optimizer == self._optimizer.Powell:
            self._registration_method.SetOptimizerAsPowell()
        elif self._optimizer == self._optimizer.Evolutionary:
            self._registration_method.SetOptimizerAsOnePlusOneEvolutionary()
        elif self._optimizer == self._optimizer.LBFGSB:
            self._registration_method.SetOptimizerAsLBFGSB()
        elif self._optimizer == self._optimizer.GradientDescent:
            self._registration_method.SetOptimizerAsGradientDescent(
                learningRate=1.0,
                numberOfIterations=300,
                convergenceMinimumValue=1e-6,
                convergenceWindowSize=10,
            )
        elif self._optimizer == self._optimizer.CGLineSearch:
            self._registration_method.SetOptimizerAsConjugateGradientLineSearch(
                2.0, 300
            )
        elif self._optimizer == self._optimizer.GradientDescentLineSearch:
            self._registration_method.SetOptimizerAsGradientDescentLineSearch(2.0, 300)
        else:
            raise ValueError(
                f"optimizer {self._optimizer} not supported by SimpleITK, choose from {[str(item) for item in list(SitkOptimizerType)]}"
            )

        # set sampling strategy
        if sampling == "random":
            self._registration_method.SetMetricSamplingStrategy(
                self._registration_method.RANDOM
            )
            self._registration_method.SetMetricSamplingPercentage(sampling_percentage)
        elif sampling == "regular":
            self._registration_method.SetMetricSamplingStrategy(
                self._registration_method.REGULAR
            )
            self._registration_method.SetMetricSamplingPercentage(sampling_percentage)

    def identity(self, dimension: int = 2) -> SimpleITKTransformation:
        return SimpleITKTransformation(
            transfo_type="identity", passive=numpy.identity(dimension + 1)
        )

    def calculate(
        self,
        from_image: numpy.ndarray,
        to_image: numpy.ndarray,
    ) -> SimpleITKTransformation:
        if self._mask is not None and numpy.any(self._mask):
            self._mask = self._mask.astype(bool)
            self._registration_method.SetMetricMovingMask(
                sitk.GetImageFromArray(self._mask.astype("uint8"))
            )
            self._registration_method.SetMetricFixedMask(
                sitk.GetImageFromArray(self._mask.astype("uint8"))
            )

        from_imageitk = sitk.GetImageFromArray(from_image)
        to_imageitk = sitk.GetImageFromArray(to_image)

        dim = from_imageitk.GetDimension()

        if self.type == self.type.translation:
            tx = sitk.TranslationTransform(dim, dim * [0])
        elif self._type in ["rigid", "similarity", "affine"]:
            if self.type == self.type.rigid and dim == 2:
                tf = sitk.Euler2DTransform()
            elif self.type == self.type.rigid and dim == 3:
                tf = sitk.Euler3DTransform()
            elif self.type == self.type.similarity and dim == 2:
                tf = sitk.Similarity2DTransform()
            elif self.type == self.type.similarity and dim == 3:
                tf = sitk.Similarity3DTransform()
            elif self.type == self.type.affine:
                tf = sitk.AffineTransform(dim)
            tx = sitk.CenteredTransformInitializer(
                to_imageitk,
                from_imageitk,
                tf,
                sitk.CenteredTransformInitializerFilter.GEOMETRY,
            )
        elif self.type == self.type.bspline:
            # Use given mesh size or put control point every 20 pixels
            if self._mesh_size:
                tx = sitk.BSplineTransformInitializer(from_imageitk, self._mesh_size)
            else:
                tx = sitk.BSplineTransformInitializer(
                    from_imageitk, [int(size / 20) for size in from_imageitk.GetSize()]
                )
        elif self.type == self.type.displacement_field:
            img = sitk.GetImageFromArray(numpy.zeros((*from_image.shape, dim)), True)
            tx = sitk.DisplacementFieldTransform(img)
            tx.SetSmoothingGaussianOnUpdate(
                varianceForUpdateField=0.0, varianceForTotalField=2.0
            )
        else:
            raise ValueError(f"{self._type} is not supported by SimpleITK")

        self._registration_method.SetInitialTransform(tx)

        if self._optimizer not in ["Powell", "GradientDescent"]:
            factors = [int(2**x) for x in numpy.arange(self._levels - 1, -1, -1)]
            self._registration_method.SetShrinkFactorsPerLevel(shrinkFactors=factors)
            self._registration_method.SetSmoothingSigmasPerLevel(
                smoothingSigmas=numpy.arange(
                    self._levels - 1, -1, -1, dtype=numpy.float64
                )
            )
        if self._optimizer != self._optimizer.LBFGSB:
            self._registration_method.SetOptimizerScalesFromPhysicalShift()
        result = self._registration_method.Execute(to_imageitk, from_imageitk)

        return SimpleITKTransformation(
            transfo_type=self._type,
            transformation=result,
        )
