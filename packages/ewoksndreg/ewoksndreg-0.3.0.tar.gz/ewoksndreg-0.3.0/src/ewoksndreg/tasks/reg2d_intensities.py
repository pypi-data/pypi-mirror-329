from ewokscore.task import Task
from ..io.input_stack import input_context
from ..intensities import registration

__all__ = ["Reg2DIntensities"]


class Reg2DIntensities(
    Task,
    input_names=["imagestack", "mapper", "transformation_type"],
    optional_input_names=[
        "mask",
        "inputs_are_stacks",
        "block_size",
        "reference",
        "preprocessing_options",
        "method_options",
    ],
    output_names=["transformations"],
):
    """Use an intensity-based registration method to calculate transformations to register the 2D-images in the stack."""

    def run(self):
        preprocessing_options = self.get_input_value("preprocessing_options", {})
        method_options = self.get_input_value("method_options", {})
        mask = self.get_input_value("mask", None)
        mapper = registration.IntensityMapping.get_subclass(self.inputs.mapper)(
            transfo_type=self.inputs.transformation_type, mask=mask, **method_options
        )
        with input_context(
            self.inputs.imagestack,
            inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
        ) as stack:
            if stack.ndim == 3:
                self.outputs.transformations = registration.calculate_transformations(
                    stack,
                    mapper,
                    reference=self.get_input_value("reference", 0),
                    block_size=self.get_input_value("block_size", 1),
                    preprocessing_options=preprocessing_options,
                )
                return
            if stack.ndim == 4:
                self.outputs.transformations = [
                    registration.calculate_transformations(
                        stack_3d,
                        mapper,
                        reference=self.get_input_value("reference", 0),
                        block_size=self.get_input_value("block_size", 1),
                        preprocessing_options=preprocessing_options,
                    )
                    for stack_3d in stack
                ]
            else:
                raise ValueError("This task only handles 3D or 4D data of 2D images")
