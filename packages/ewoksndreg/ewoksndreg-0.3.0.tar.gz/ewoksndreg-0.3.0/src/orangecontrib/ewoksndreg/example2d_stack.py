from contextlib import contextmanager

from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import Example2DStack
from ewoksndreg.transformation.types import TransformationType
from ewoksndreg.io.input_stack import input_context

try:
    import skimage
except ImportError:
    skimage = None


__all__ = ["OWExample2DStack"]


class OWExample2DStack(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Example2DStack
):
    name = "2D Example Stack"
    description = "Generate a stack of 2D example images"
    icon = "icons/load_stack.svg"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        options = {
            "name": {
                "value_for_type": [
                    "astronaut",
                    "camera",
                    "brick",
                    "grass",
                    "gravel",
                    "cell",
                ]
            },
            "transformation_type": {
                "value_for_type": list(TransformationType.__members__),
                "serialize": str,
            },
            "nimages": {"value_for_type": 0},
            "shape": {
                "value_for_type": "",
                "serialize": lambda tpl: ",".join(list(map(str, tpl))),
                "deserialize": lambda s: tuple(map(int, s.split(","))),
            },
            "add_noise_dim": {
                "value_for_type": False,
                "enabled": bool(skimage),
                "label": "Add noise dimension",
            },
        }

        for name, kw in options.items():
            self._default_inputs_form.addParameter(
                name,
                value=values[name],
                value_change_callback=self._default_inputs_changed,
                **kw,
            )

    def _default_inputs_changed(self):
        self.update_default_inputs(**self._default_inputs_form.get_parameter_values())
        self._update_input_data()

    def handleNewSignals(self) -> None:
        self._update_input_data()
        super().handleNewSignals()

    def task_output_changed(self):
        self._update_output_data()

    def _init_main_area(self):
        super()._init_main_area()
        layout = self._get_main_layout()
        self._plot = Plot2D(parent=self.mainArea)
        layout.addWidget(self._plot)
        self._slider1 = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._slider1)
        self._slider1.valueChanged[int].connect(lambda: self._select_output_image())
        self._slider2 = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._slider2)
        self._slider2.valueChanged[int].connect(lambda: self._select_output_image())
        self._slider2.setVisible(False)
        self._update_output_data()

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

    @contextmanager
    def _output_context(self, images=None):
        if images is not None:
            yield images
            return
        try:
            with input_context(self.get_task_output_value("imagestack")) as images:
                yield images
        except TypeError:
            yield None

    def _update_output_data(self):
        with self._output_context() as images:
            if images is None:
                return

            assert images.ndim in (3, 4)

            if images.ndim == 4:
                self._slider1.setMaximum(max(images.shape[0] - 1, 0))
                self._slider2.setVisible(True)
                self._slider2.setMaximum(max(images.shape[1] - 1, 0))
            else:
                self._slider2.setVisible(False)
                self._slider1.setMaximum(max(images.shape[0] - 1, 0))
            self._select_output_image(images=images)

    def _select_output_image(self, images=None):
        if self._slider2.isVisible():
            selection = (self._slider1.value(), self._slider2.value())
        else:
            selection = self._slider1.value()
        with self._output_context(images=images) as images:
            if images:
                self._plot.addImage(images[selection], legend="image")
