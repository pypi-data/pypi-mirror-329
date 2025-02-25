"""Data to test registration"""

from typing import Tuple, List
import numpy

try:
    from skimage import data
    from skimage.transform import warp
    from skimage.transform import SimilarityTransform
    from skimage.transform import AffineTransform, ProjectiveTransform
    from skimage.color import rgb2gray
    from skimage.util import img_as_float
    from skimage.filters import gaussian
except ImportError:
    data = None

try:
    import SimpleITK as sitk
except ImportError:
    sitk = False

from ...math.normalization import stack_range_normalization
from ...transformation.types import TransformationType


def images(
    transfo_type: TransformationType,
    shape: Tuple[int, int] = (200, 220),
    nimages: int = 4,
    plot: float = 0,
    name: str = "astronaut",
) -> Tuple[List[numpy.ndarray], List[numpy.ndarray], List[numpy.ndarray]]:
    if data is None:
        raise ModuleNotFoundError("No module named 'skimage'")
    load_image = getattr(data, name)
    image0 = load_image()
    if image0.ndim > 2:
        image0 = rgb2gray(image0)
    image0 = img_as_float(image0)
    image0 = image0[::-1, :]
    full_shape = numpy.array(image0.shape)
    if all(shape):
        sub_shape = numpy.minimum(numpy.array(shape), full_shape)
    else:
        sub_shape = full_shape
    center = (full_shape / 2).astype(int)
    d = (sub_shape / 2).astype(int)
    idx0 = center - d
    idx1 = center + d
    idx = tuple(slice(i0, i1) for i0, i1 in zip(idx0, idx1))

    if transfo_type == TransformationType.identity:
        tform = SimilarityTransform()
    elif transfo_type == TransformationType.translation:
        tform = SimilarityTransform(translation=[2, 3])
    elif transfo_type == TransformationType.rigid:
        tform = SimilarityTransform(rotation=numpy.radians(4))
    elif transfo_type == TransformationType.similarity:
        tform = SimilarityTransform(scale=1.05)
    elif transfo_type == TransformationType.affine:
        tform = AffineTransform(shear=numpy.radians(4))
    elif transfo_type == TransformationType.projective:
        matrix = numpy.array([[1, 0, 0], [0, 1, 0], [0.001, 0.001, 1]])
        tform = ProjectiveTransform(matrix=matrix)
    elif transfo_type == TransformationType.bspline:
        return get_bspline(image0, nimages, idx)
    elif transfo_type == TransformationType.displacement_field:
        return get_deformations(image0, nimages, idx)

    else:
        raise NotImplementedError(transfo_type)

    tbefore = SimilarityTransform(translation=-center[::-1])
    tafter = SimilarityTransform(translation=center[::-1])

    change_orig1 = SimilarityTransform(translation=idx0[::-1])
    change_orig2 = SimilarityTransform(translation=-idx0[::-1])
    tform0 = tbefore + tform + tafter

    image1 = image0.copy()
    tform1 = tform0
    images = [image1[idx]]
    passive = [numpy.identity(3)]
    active = [numpy.identity(3)]
    if plot:
        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.imshow(images[-1], origin="lower")
        plt.pause(plot)
    for _ in range(1, nimages):
        image1 = warp(image0, tform1, order=3)
        images.append(image1[idx])
        active.append(indexing_order((change_orig1 + tform1 + change_orig2).params))
        passive.append(
            indexing_order(
                numpy.linalg.inv((change_orig1 + tform1 + change_orig2).params)
            )
        )
        if plot:
            fig.clear()
            plt.imshow(images[-1], origin="lower")
            plt.pause(plot)
        tform1 = tform1 + tform0

    return images, active, passive


def get_deformations(
    image: numpy.ndarray, nimages: int, idx: Tuple[slice]
) -> Tuple[List[numpy.ndarray], List[numpy.ndarray], List[numpy.ndarray]]:
    images = [image[idx]]
    if not sitk:
        raise ModuleNotFoundError("No module named 'SimpleITK'")
    simage = sitk.GetImageFromArray(image)
    shape = image.shape
    deformation = (numpy.random.rand(*shape, 2) - 0.5) * 10
    passive = [numpy.zeros_like(deformation)]
    active = [numpy.zeros_like(deformation)]
    for i in range(nimages):
        active.append(gaussian(deformation * (1.5 * i + 1), i / 4 + 1))
        field = sitk.GetImageFromArray(active[-1], True)
        passive.append(sitk.GetArrayFromImage(sitk.InvertDisplacementField(field)))

        displ = sitk.DisplacementFieldTransform(field)
        result = sitk.Resample(
            simage, simage, displ, sitk.sitkBSpline1, 0.0, simage.GetPixelID()
        )
        images.append(sitk.GetArrayFromImage(result)[idx])
    for i in range(len(passive)):
        passive[i] = passive[i][idx]
        active[i] = active[i][idx]
    return images, active, passive


def get_bspline(
    image: numpy.ndarray, nimages: int, idx: Tuple[slice]
) -> Tuple[List[numpy.ndarray], List[numpy.ndarray], List[numpy.ndarray]]:
    if not sitk:
        raise ModuleNotFoundError("No module named 'SimpleITK'")
    images = [image[idx]]

    simage = sitk.GetImageFromArray(images[0])
    shape = image.shape
    spline_order = 3
    mesh_size = [int(i / 20) for i in shape]
    npoints = [m + spline_order for m in mesh_size]

    displacements = numpy.random.rand(numpy.prod(npoints) * 2) - 0.5
    transform = sitk.BSplineTransformInitializer(simage, mesh_size, 3)
    passive = [numpy.zeros((*shape, 2))]
    active = [[*transform.GetCoefficientImages(), 3]]
    for i in range(nimages):
        scaled = displacements * (i + 1)
        transform.SetParameters(scaled)
        active.append([*transform.GetCoefficientImages(), 3])
        field = sitk.TransformToDisplacementField(
            transform,
            outputPixelType=sitk.sitkVectorFloat64,
            size=simage.GetSize(),
            outputOrigin=simage.GetOrigin(),
            outputSpacing=simage.GetSpacing(),
            outputDirection=simage.GetDirection(),
        )

        passive.append(sitk.GetArrayFromImage(sitk.InvertDisplacementField(field)))
        result = sitk.Resample(
            simage, simage, transform, sitk.sitkBSpline1, 0.0, simage.GetPixelID()
        )
        images.append(sitk.GetArrayFromImage(result))

    return images, active, passive


def noisy_imagestacks(
    transfo_type: TransformationType, nstacks: int = 3, nimages: int = 4
) -> numpy.ndarray:
    stack, _, _ = images(transfo_type, nimages=nimages)
    stack = numpy.stack(stack)
    noise = numpy.random.random(stack.shape)
    stacks = [
        stack_range_normalization(stack + noise * i)
        for i in numpy.linspace(0, 0.5, nstacks)
    ]
    return stacks


def indexing_order(matrix: numpy.ndarray) -> numpy.ndarray:
    matrix = matrix.copy()
    matrix[:2, :2] = matrix[:2, :2].T
    matrix[:2, 2] = matrix[:2, 2][::-1]
    return matrix
