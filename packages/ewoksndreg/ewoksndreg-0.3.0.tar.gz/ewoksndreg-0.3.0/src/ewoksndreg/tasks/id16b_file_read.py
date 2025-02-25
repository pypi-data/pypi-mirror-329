import fabio
from ..tests.data.read import getfiles
from ..io.output_stack import output_context
from ewokscore import Task


class ID16BFileRead(
    Task,
    input_names=["scandir", "recsuffix"],
    optional_input_names=["url", "normalize"],
    output_names=["imagestack"],
):
    def run(self):
        scandir = self.get_input_value("scandir", None)
        recsuffix = self.get_input_value("recsuffix", None)
        url = self.get_input_value("url", None)
        normalize = self.get_input_value("normalize", False)
        energies, files = getfiles(scandir, recsuffix)
        with output_context(url=url) as ostack:
            for filename, energy in zip(files, energies):
                with fabio.open(filename) as f:
                    image = f.data
                    if normalize:
                        image = (image - image.min()) / (image.max() - image.min())
                    ostack.add_point(image)
            if url is not None:
                self.outputs.imagestack = url
            else:
                self.outputs.imagestack = ostack.data
