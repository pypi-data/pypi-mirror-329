from typing import Optional, Sequence, List, Tuple
from ..io.input_stack import InputStack
from ..transformation.base import Transformation
from .features.base import Features
from .detection.base import FeatureDetector
from .matching.base import FeatureMatching
from .mapping.base import FeatureMapping


def detect_features(
    input_stack: InputStack,
    detector: FeatureDetector,
    include: Optional[Sequence[int]] = None,
) -> List[Features]:
    if include is None:
        include = list(range(len(input_stack)))
    return [detector.find(input_stack[i]) for i in include]


def match_features(
    input_stack: InputStack,
    features: List[Features],
    matcher: FeatureMatching,
    include: Optional[Sequence[int]] = None,
    reference: int = 0,
) -> List[Tuple[Features, Features]]:
    if include is None:
        include = list(range(len(input_stack)))
    ref_features = features[reference]
    matches = list()
    ref_image = input_stack[reference]
    for i in include:
        new_image = input_stack[i]
        if i == reference:
            matches.append((None, None))
        else:
            matches.append(
                matcher.match(ref_features, features[i], ref_image, new_image)
            )
    return matches


def transformations_from_features(
    matches: List[Optional[Tuple[Features, Features]]], mapper: FeatureMapping
) -> List[Transformation]:
    transformations = list()
    for ref_features, new_features in matches:
        if ref_features:
            transformations.append(mapper.calculate(new_features, ref_features))
        else:
            transformations.append(mapper.identity())
    return transformations


def calculate_transformations(
    input_stack: InputStack,
    detector: FeatureDetector,
    matcher: FeatureMatching,
    mapper: FeatureMapping,
    include: Optional[Sequence[int]] = None,
    reference: int = 0,
) -> List[Transformation]:
    features = detect_features(input_stack, detector, include=include)
    matches = match_features(
        input_stack, features, matcher, include=include, reference=reference
    )
    return transformations_from_features(matches, mapper)
