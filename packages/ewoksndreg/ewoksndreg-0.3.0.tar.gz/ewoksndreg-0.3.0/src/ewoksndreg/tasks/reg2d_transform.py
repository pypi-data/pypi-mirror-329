from ewokscore.task import Task
from ..io.input_stack import input_context
from ..io.output_stack import output_context
from ..transformation import apply_transformations, Transformation
from ..transformation import SciKitImageHomography

from os.path import join
from silx.io.url import DataUrl

import numpy as np
from itertools import cycle
from typing import Union, Sequence

__all__ = ["Reg2DTransform"]


class Reg2DTransform(
    Task,
    input_names=["imagestack", "transformations"],
    optional_input_names=[
        "url",
        "inputs_are_stacks",
        "crop",
        "interpolation_order",
        "stack_names",
    ],
    output_names=["imagestack"],
):
    """Apply transformations calculated from image registration to images."""

    def run(self):
        url = self.get_input_value("url", None)
        crop = self.get_input_value("crop", False)
        interpolation_order = self.get_input_value("interpolation_order", 1)
        stack_names = self.get_input_value("stack_names", None)

        # the transformations are either type Transformation or np.ndarray(homography matrices)
        transfos = as_transformations(self.inputs.transformations)

        with input_context(
            self.inputs.imagestack,
            inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
        ) as istack:
            if istack.ndim == 3:
                if isinstance(transfos[0], np.ndarray):
                    transfos = [SciKitImageHomography(tr) for tr in transfos]
                if len(transfos) != len(istack):
                    raise ValueError(
                        "Amount of transformations and images doesn't match"
                    )
                with output_context(url=url) as ostack:
                    apply_transformations(
                        istack,
                        ostack,
                        transfos,
                        crop=crop,
                        interpolation_order=interpolation_order,
                    )
                    if url:
                        self.outputs.imagestack = url
                    else:
                        self.outputs.imagestack = ostack.data
                return

            if stack_names is None:
                stack_names = [str(i) for i in range(len(istack))]
            stack_names = [name + "_aligned" for name in stack_names]
            if isinstance(transfos[0], (np.ndarray, Transformation)):
                transfos = [transfos]
            else:
                if crop:
                    raise ValueError(
                        "Cropping when applying multiple different lists not supported because of differing image sizes"
                    )

            # we have a list of list of transformations and a list of stacks
            if len(transfos[0]) != len(istack[0]):
                raise ValueError(
                    "Amount of transformations and images per stack doesn't match"
                )
            if not (len(transfos) == 1 or len(transfos) == len(istack)):
                raise ValueError(
                    "Amount of imagestacks and transformationstacks doesn't match"
                )
            data = []
            for stack, transfo, name in zip(istack, cycle(transfos), stack_names):
                if url:
                    # append `name` to the url
                    dataurl = DataUrl(url)
                    dpath = dataurl.data_path()
                    if dpath is None:
                        dpath = "/"
                    dpath = join(dpath, name)
                    full_url = DataUrl(
                        file_path=dataurl.file_path(), data_path=dpath
                    ).path()
                else:
                    full_url = None
                with output_context(url=full_url) as ostack:
                    apply_transformations(
                        stack,
                        ostack,
                        transfo,
                        crop=crop,
                        interpolation_order=interpolation_order,
                    )
                    if full_url:
                        data.append(full_url)
                    else:
                        data.append(np.asarray(ostack.data))

            self.outputs.imagestack = data


def as_transformations(
    transformations: Union[
        Sequence[np.ndarray],
        Sequence[Transformation],
        Sequence[Sequence[Transformation]],
        Sequence[Sequence[np.ndarray]],
    ],
) -> Union[Sequence[Transformation], Sequence[Sequence[Transformation]]]:
    if isinstance(transformations[0], np.ndarray):
        return [SciKitImageHomography(transfo) for transfo in transformations]

    if isinstance(transformations[0], Sequence) and isinstance(
        transformations[0][0], np.ndarray
    ):
        return [[SciKitImageHomography(t) for t in seq] for seq in transformations]

    return transformations
