from enum import Enum


class TransformationType(str, Enum):
    identity = "identity"
    translation = "translation"
    rigid = "rigid"
    similarity = "similarity"
    affine = "affine"
    projective = "projective"
    bspline = "bspline"
    displacement_field = "displacement_field"
    composite = "composite"
