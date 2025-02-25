from typing import Optional, Sequence, List
from ..io.input_stack import InputStack
from ..io.output_stack import OutputStack
from .base import Transformation
from ..math.crop import calc_NaN_edges
import numpy


def apply_transformations(
    input_stack: InputStack,
    output_stack: OutputStack,
    transformations: List[Transformation],
    include: Optional[Sequence[int]] = None,
    cval: int = numpy.nan,
    crop: bool = False,
    interpolation_order: int = 1,
):
    if include is None:
        include = range(len(transformations))
    else:
        if len(include) != len(transformations):
            raise ValueError(
                "Number of transformations and number of items to transform must be the same"
            )

    # calculate slices for cropping
    only_translations = all(
        [x.type in ["identity", "translation"] for x in transformations]
    )
    img_shape = input_stack[0].shape
    low = (0, 0)
    high = (img_shape[0], img_shape[1])
    if crop:
        if only_translations:
            for i in include:
                transformed = transformations[i].apply_data(
                    input_stack[i],
                    offset=None,
                    shape=None,
                    cval=cval,
                    interpolation_order=interpolation_order,
                )
                new_low, new_high = calc_NaN_edges(transformed)
                low = [max(l1, l2) for l1, l2 in zip(low, new_low)]
                high = [min(h1, h2) for h1, h2 in zip(high, new_high)]

        else:
            raise ValueError(
                "Can't meaningfully crop based on transformations that are not translations"
            )

    for i in include:
        transformed = transformations[i].apply_data(
            input_stack[i],
            offset=None,
            shape=None,
            cval=cval,
            interpolation_order=interpolation_order,
        )
        transformed = transformed[low[0] : high[0], low[1] : high[1]]

        output_stack.add_point(transformed)
