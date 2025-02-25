from typing import Tuple, Optional, Mapping, Dict
from numbers import Number
import numpy
from .base import FeatureMatching
from ..features import Features
from ..features import NumpyKeypointFeatures

__all__ = ["NumpyKeypointFeatureMatching"]


class NumpyKeypointFeatureMatching(
    FeatureMatching,
    registry_id=FeatureMatching.RegistryId("Keypoint", "Numpy"),
    register=False,
):
    def __init__(self, match_options: Optional[Mapping] = None, **kw) -> None:
        if match_options is None:
            match_options = dict()
        match_options.setdefault("npoints", 8)
        self._match_options = match_options
        super().__init__(**kw)

    def match(
        self,
        from_features: Features,
        to_features: Features,
        from_image: numpy.ndarray,
        to_image: numpy.ndarray,
    ) -> Tuple[Features, Features]:
        numpy_from_features = from_features.as_type(NumpyKeypointFeatures)
        numpy_to_features = to_features.as_type(NumpyKeypointFeatures)
        idx_from, idx_to = match_keypoints(
            numpy_from_features,
            numpy_to_features,
            from_image,
            to_image,
            **self._match_options,
        ).T
        return (from_features[idx_from], to_features[idx_to])


def match_keypoints(
    features1: NumpyKeypointFeatures,
    features2: NumpyKeypointFeatures,
    image1: numpy.ndarray,
    image2: numpy.ndarray,
    window_ext=5,
    gauss_sigma=3,
    npoints=None,
    metric="nssd",
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Match features based differences between ROI's around
    their coordinates.

    This method returns two arrays:

     - an array of matching indices in `features1` and `features2`
     - an array of matching measures (smaller value means a better match)

    These two arrays are sorted by increasing matching measure.

    The following difference measures are supported:
        - sum of squared differences
    """

    # TODO: add more measures
    # https://towardsdatascience.com/measuring-similarity-in-two-images-using-python-b72233eb53c6
    if image1.shape != image2.shape:
        raise ValueError("'image1' and 'image2' shape do not match")
    wmax = 2 * window_ext + 1
    if image1.shape[0] < wmax or image1.shape[1] < wmax:
        raise ValueError("'window_ext' too large for image shape")

    start1, stop1 = _extract_rois(features1.coordinates, image1.shape, window_ext)
    stack1 = numpy.stack(
        [
            image1[idx_start[0] : idx_stop[0], idx_start[1] : idx_stop[1]]
            for idx_start, idx_stop in zip(start1.T, stop1.T)
        ],
        axis=0,
    )

    start2, stop2 = _extract_rois(features2.coordinates, image2.shape, window_ext)
    stack2 = numpy.stack(
        [
            image1[idx_start[0] : idx_stop[0], idx_start[1] : idx_stop[1]]
            for idx_start, idx_stop in zip(start2.T, stop2.T)
        ],
        axis=0,
    )

    if gauss_sigma:
        weights = _gaussian_weights(window_ext, gauss_sigma)
    else:
        weights = numpy.zeros(wmax, wmax)
    try:
        fmetric = _METRICS[metric]
    except KeyError:
        raise ValueError(f"Unknown image similarity metric '{metric}'")
    dmeas = numpy.vstack(
        [[fmetric(roi1, roi2, weights) for roi2 in stack2] for roi1 in stack1]
    )

    match0 = _matching_indices(dmeas, ref_axis=0)
    match1 = _matching_indices(dmeas, ref_axis=1)
    avgmeas0 = sum(match0.values()) / len(match0)
    avgmeas1 = sum(match1.values()) / len(match1)
    totmeas = avgmeas0 + avgmeas1
    if totmeas:
        w0 = avgmeas0 / totmeas
        w1 = avgmeas1 / totmeas
    else:
        w0 = 0.5
        w1 = 0.5
    match = {
        idx: w0 * match0[idx] + w1 * match1[idx] for idx in match0 if idx in match1
    }
    indices, _ = zip(*sorted(match.items(), key=lambda item: item[1]))
    if npoints:
        indices = indices[:npoints]
    return numpy.array(indices)


def _normalize(image: numpy.ndarray) -> numpy.ndarray:
    mi = numpy.nanmin(image)
    ma = numpy.nanmax(image)
    if mi == ma:
        return image
    return (image - mi) / (ma - mi)


def _gaussian_weights(window_ext: int, sigma=1):
    y, x = numpy.mgrid[-window_ext : window_ext + 1, -window_ext : window_ext + 1]
    g = numpy.zeros(y.shape, dtype=numpy.double)
    g[:] = numpy.exp(-0.5 * (x**2 / sigma**2 + y**2 / sigma**2))
    g /= 2 * numpy.pi * sigma * sigma
    return g


def _extract_rois(
    coordinates: numpy.ndarray, shape: Tuple[int, int], window_ext: int
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    shape = numpy.array(shape).reshape((2, 1))
    coordinates = numpy.round(coordinates).astype(int)
    kpstart = coordinates - window_ext
    kpstop = coordinates + window_ext + 1

    wmax = 2 * window_ext + 1

    for dim, idx in enumerate(kpstart < 0):
        kpstart[dim, idx] = 0
        kpstop[dim, idx] = wmax

    for dim, idx in enumerate(kpstop > shape):
        kpstart[dim, idx] = shape[dim] - wmax
        kpstop[dim, idx] = shape[dim]

    return kpstart, kpstop


def _nssd_metric(
    image1: numpy.ndarray, image2: numpy.ndarray, weights: numpy.ndarray
) -> numpy.ndarray:
    return (weights * (_normalize(image1) - _normalize(image2)) ** 2).sum()


_METRICS = {"nssd": _nssd_metric}


def _matching_indices(
    dmeas: numpy.ndarray, ref_axis=0
) -> Dict[Tuple[Number, Number], Number]:
    """Matching means smallest similarity metric.

    :param dmeas: 2D array with similarity metric (number >= 0) between 2 sets of items
    :returns: map matching index pairs to the corresponding similarity metric
    """
    match_axis = 1 - ref_axis
    ref_idx = range(dmeas.shape[ref_axis])
    match_idx = numpy.argmin(dmeas, axis=match_axis)
    if ref_axis == 0:
        idx0 = ref_idx
        idx1 = match_idx
    else:
        idx0 = match_idx
        idx1 = ref_idx
    return {(i0, i1): dmeas[i0, i1] for i0, i1 in zip(idx0, idx1)}
