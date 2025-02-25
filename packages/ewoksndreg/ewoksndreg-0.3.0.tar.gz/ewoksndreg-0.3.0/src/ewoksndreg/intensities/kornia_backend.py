import kornia
import numpy
import torch
import torch.nn.functional as F
import torch.optim as opt

from .base import IntensityMapping
from ..transformation.types import TransformationType
from ..transformation.base import Transformation
from ..transformation.homography import Homography, reverse_indices
from ..transformation.scikitimage_backend import SciKitImageHomography
from .torch_metrics import nmi_loss
from .types import KorniaMetricType, KorniaOptimizerType


class KorniaOptimizationIntensityMapping(
    IntensityMapping,
    registry_id=IntensityMapping.RegistryId("Optimization", "Kornia"),
):
    SUPPORTED_TRANSFORMATIONS = ["translation", "similarity", "projective"]

    def __init__(
        self,
        transfo_type: TransformationType,
        metric: KorniaMetricType = "MeanSquaredError",
        optimizer: KorniaOptimizerType = "RMSprop",
        pyramid_levels: int = 3,
        **kw,
    ) -> None:
        super().__init__(transfo_type, **kw)

        # set transformation type
        if self._type == "projective":
            ktype = "homography"
        else:
            ktype = self._type

        # set metric
        if metric == "MeanAbsoluteError":
            loss_fn = F.l1_loss
        elif metric == "MeanSquaredError":
            loss_fn = F.mse_loss
        elif metric == "MutualInformation":
            loss_fn = nmi_loss
        else:
            raise ValueError(
                f"Invalid Metric, got {metric}, choose one in {[str(item) for item in list(KorniaMetricType)]}"
            )

        # set optimizer
        if optimizer == "SGD":
            optimizer = opt.SGD
        elif optimizer == "Adam":
            optimizer = opt.Adam
        elif optimizer == "RMSprop":
            optimizer = opt.RMSprop
        else:
            raise ValueError(
                f"Invalid Optimizer, got {optimizer}, choose one in {[str(item) for item in list(KorniaOptimizerType)]}"
            )
        self._registrator = kornia.geometry.ImageRegistrator(
            ktype,
            optimizer=optimizer,
            loss_fn=loss_fn,
            pyramid_levels=pyramid_levels,
            tolerance=0.000001,
            num_iterations=200,
        )

    def calculate(
        self, from_image: numpy.ndarray, to_image: numpy.ndarray
    ) -> Homography:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        shp = from_image.shape

        if device == "cuda":
            from_tensor = torch.tensor(from_image, device=device)
            to_tensor = torch.tensor(to_image, device=device)
        else:
            from_tensor = torch.from_numpy(from_image)
            to_tensor = torch.from_numpy(to_image)

        from_tensor = from_tensor.reshape(1, 1, *from_tensor.size())
        to_tensor = to_tensor.reshape(1, 1, *to_tensor.size())

        transformation = self._registrator.register(
            from_tensor.float(), to_tensor.float(), verbose=False
        )

        transformation = reverse_indices(
            numpy.squeeze(transformation.detach().cpu().numpy())
        )
        """
        calculated transformation uses coordinates in range [-1,1]x[-1,1],
        so we need to first transform from our coordinate system to the one used by the transformation (that's pre)
        and afterwards we need to transform back (thats both post transformations)
        """
        pre = numpy.array([[2 / shp[0], 0, -1], [0, 2 / shp[1], -1], [0, 0, 1]])
        post = numpy.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]])
        post2 = numpy.array([[shp[0] / 2, 0, 0], [0, shp[1] / 2, 0], [0, 0, 1]])
        full = post2 @ post @ transformation @ pre
        return SciKitImageHomography(full, transfo_type=self._type)

    def identity(self, dimension: int = 2) -> Transformation:
        return SciKitImageHomography(
            numpy.identity(dimension + 1), TransformationType.identity
        )
