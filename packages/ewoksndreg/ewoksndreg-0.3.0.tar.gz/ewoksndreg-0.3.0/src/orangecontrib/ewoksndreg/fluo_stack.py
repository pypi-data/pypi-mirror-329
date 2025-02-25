from contextlib import contextmanager

from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import FluoStack
from ewoksndreg.io.input_stack import input_context


__all__ = ["OWFluoStack"]


class OWFluoStack(OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=FluoStack):
    name = "ID21 Fluo Stack"
    description = "Calculate transformations of a stack of images based on features"
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
            "path": {"value_for_type": "", "select": "file"},
            "stack": {
                "value_for_type": "absorp1",
                "serialize": str,
            },
            "exclude": {
                "value_for_type": "",
                "serialize": str,
            },
            "normalize": {
                "value_for_type": False,
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
        self._plot.setDefaultColormap(Colormap("viridis"))
        layout.addWidget(self._plot)
        self._slider = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._slider)
        self._slider.valueChanged[int].connect(self._select_output_image)
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
            binit = True
            with input_context(self.get_task_output_value("imagestack")) as images:
                binit = False
                yield images
        except TypeError:
            if binit:
                yield list()

    def _update_output_data(self):
        with self._output_context() as images:
            self._slider.setMaximum(max(len(images) - 1, 0))
            self._select_output_image(self._slider.value(), images=images)

    def _select_output_image(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                self._plot.addImage(images[select], legend="image")
