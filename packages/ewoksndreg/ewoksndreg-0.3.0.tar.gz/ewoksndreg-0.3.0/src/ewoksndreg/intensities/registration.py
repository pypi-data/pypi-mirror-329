from typing import Optional, Sequence, List, Dict
from ..io.input_stack import InputStack
from ..transformation.base import Transformation
from ..math.filter import preprocess
from .base import IntensityMapping


def calculate_transformations(
    input_stack: InputStack,
    mapper: IntensityMapping,
    include: Optional[Sequence[int]] = None,
    reference: int = 0,
    block_size: int = 1,
    preprocessing_options: Optional[Dict] = None,
) -> List[Transformation]:
    """
    Uses the mapper to calculate the transformation between the reference image and all other images in the stack.

    param input_stack: InputStack of all the images
    param mapper: An IntensityMapper to calculate transformations between the images
    param include: Indices of images to include for the registration. Default: all.
    param reference: The index of the reference image, if -1 the reference will be the middle of the stack
    param block_size: Included images get partitioned into blocks.Every image in one block gets aligned to the first element in the block.The first elements of each block get sequentially aligned to the reference

    """
    if include is None:
        include = list(range(len(input_stack)))
    if block_size <= 0:
        block_size = 1
    if reference == -1:
        reference = len(input_stack) // 2
    if reference < -1 or reference >= len(input_stack):
        raise ValueError(
            f"Please use a valid index between 0 and {len(input_stack)} or -1"
        )
    if preprocessing_options is None:
        preprocessing_options = {}
    # ref_index is the index of the reference in include, as include might not contain all indices
    ref_index = include.index(reference)
    ref_image = preprocess(input_stack[reference], **preprocessing_options)
    dim = ref_image.ndim
    transformations = [mapper.identity(dim)]

    # calculate all transformations up to reference
    # counter holds the position in one block, so goes from 0 to block_size-1
    counter = 0
    current_ref_transfo = mapper.identity(dim)
    for i in reversed(include[:ref_index]):
        next_img = preprocess(input_stack[i], **preprocessing_options)
        next_transfo = mapper.calculate(next_img, ref_image) * current_ref_transfo
        counter += 1
        transformations.append(next_transfo)
        if counter % block_size == 0:
            ref_image = next_img
            current_ref_transfo = next_transfo
            counter = 0

    transformations = list(reversed(transformations))

    # calculate all transformations after reference
    ref_image = input_stack[reference]
    counter = 0
    current_ref_transfo = mapper.identity(dim)
    for i in include[ref_index + 1 :]:
        next_img = preprocess(input_stack[i], **preprocessing_options)
        next_transfo = mapper.calculate(next_img, ref_image) * current_ref_transfo
        transformations.append(next_transfo)
        counter += 1
        if counter % block_size == 0:
            ref_image = next_img
            current_ref_transfo = next_transfo
            counter = 0

    return transformations
