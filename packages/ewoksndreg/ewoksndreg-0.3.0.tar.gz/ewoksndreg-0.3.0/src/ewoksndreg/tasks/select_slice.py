from ewokscore.task import Task
from ..io.input_stack import input_context
from ..io.output_stack import output_context

__all__ = ["SelectSlice"]


class SelectSlice(
    Task,
    input_names=["imagestack"],
    optional_input_names=["inputs_are_stacks", "url", "x", "y", "z"],
    output_names=["imagestack"],
):
    """Slice out a subvolume of the imagestack"""

    def run(self):
        url = self.get_input_value("url", None)
        with output_context(url=url) as ostack:
            with input_context(
                self.inputs.imagestack,
                inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
            ) as istack:
                shape = istack.shape

                x = self.get_input_value("x", f"0:{shape[1]}")
                y = self.get_input_value("y", f"0:{shape[2]}")
                z = self.get_input_value("z", f"0:{shape[0]}")

                x = parse(x)
                y = parse(y)
                z = parse(z)
                ostack.add_points([img[y, x] for img in istack[z]])

                if url:
                    self.outputs.imagestack = url
                else:
                    self.outputs.imagestack = ostack.data


def parse(string: str):
    return slice(
        *map(lambda x: int(x.strip()) if x.strip() else None, string.split(":"))
    )
