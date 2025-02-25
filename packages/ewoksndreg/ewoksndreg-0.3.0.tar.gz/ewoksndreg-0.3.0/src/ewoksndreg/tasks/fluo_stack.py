from ewokscore.task import Task
import numpy as np
from ..tests.data.data_from_h5 import calculate_exclusions, get_stack, get_all_stacks
from ..math.normalization import stack_range_normalization, range_normalization

__all__ = ["FluoStack", "FluoAllStacks"]


class FluoStack(
    Task,
    input_names=["path", "stack"],
    optional_input_names=["exclude", "normalize"],
    output_names=["imagestack", "stack_name", "energies"],
):
    """Fetch a stack of images corresponding to the given counter from the given h5 file"""

    def run(self):
        values = self.get_input_values()
        path = values.pop("path")
        stack = values.pop("stack")
        normalize = values.pop("normalize", False)
        exclude = self.get_input_value("exclude", None)

        exclusions = calculate_exclusions(exclude)

        images, energies = get_stack(path, stack, exclusions)

        images = np.array(images)
        if normalize:
            images = stack_range_normalization(images)
        self.outputs.imagestack = images
        self.outputs.stack_name = stack
        self.outputs.energies = energies


class FluoAllStacks(
    Task,
    input_names=["path"],
    optional_input_names=["exclude", "normalize", "stack_names"],
    output_names=["imagestacks", "stack_names"],
):
    """Fetch all of the different counters from a given h5 file"""

    def run(self):
        values = self.get_input_values()
        path = values.pop("path")
        stack_names = [
            "absorp1",
            "absorp2",
            "absorp3",
            "idet",
            "fluo1",
            "fluo2",
            "fx2_det0_AlKa",
            "fx2_det0_BaL1",
            "fx2_det0_BiM",
            "fx2_det0_CaKa",
            "fx2_det0_CdL",
            "fx2_det0_CeL",
            "fx2_det0_ClKa",
            "fx2_det0_CoKa",
            "fx2_det0_CrKa",
            "fx2_det0_CuKa",
            "fx2_det0_FeKa",
            "fx2_det0_HgM",
            "fx2_det0_ILb",
            "fx2_det0_KKa",
            "fx2_det0_MgKa",
            "fx2_det0_MnKa",
            "fx2_det0_NiKa",
            "fx2_det0_PdL",
            "fx2_det0_PKa",
            "fx2_det0_PtM",
            "fx2_det0_SbL1",
            "fx2_det0_SbL2",
            "fx2_det0_SiKa",
            "fx2_det0_SKa",
            "fx2_det0_SnL",
            "fx2_det0_SnL1",
            "fx2_det0_SrL",
            "fx2_det0_SrL1",
            "fx2_det0_TaM",
            "fx2_det0_TbLa",
            "fx2_det0_TbLb",
            "fx2_det0_TeL2",
            "x2_det0_TeL3",
            "fx2_det0_TiKa",
            "fx2_det0_VKa",
            "fx2_det0_ZnKa",
        ]
        selection = self.get_input_value("stack_names", stack_names)
        if not isinstance(selection[0], str):
            selection = [stack_names[i] for i in selection]
        exclude = values.pop("exclude", None)
        exclusions = calculate_exclusions(exclude)
        images = get_all_stacks(path, selection, exclusions)

        if self.get_input_value("normalize", True):
            for scan in images.keys():
                for counter in images[scan].keys():
                    images[scan][counter] = range_normalization(images[scan][counter])

        self.outputs.stack_names = list(images[list(images)[0]])
        images = [list(scan.values()) for scan in images.values()]
        images = np.array(images).transpose((1, 0, 2, 3))
        self.outputs.imagestacks = images
