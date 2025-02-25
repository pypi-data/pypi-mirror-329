from contextlib import contextmanager

from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import FluoAllStacks
from ewoksndreg.io.input_stack import input_context, InputStackNumpy


__all__ = ["OWFluoAllStacks"]


class OWFluoAllStacks(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=FluoAllStacks
):
    name = "ID21 Fluo All Stacks"
    description = (
        "Get a dictionary of all stacks using the provided path to the dataset"
    )
    icon = "icons/load_stacks.svg"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()
        self.current_stack = 0
        self.current_image = 0

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        options = {
            "path": {
                "value_for_type": "",
                "select": "file",
            },
            "exclude": {
                "value_for_type": "",
                "serialize": str,
            },
            "normalize": {
                "value_for_type": True,
            },
        }
        values["normalize"] = True
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
        self._slider.valueChanged[int].connect(self._select_output_stack)
        self._slider2 = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._slider2)
        self._slider2.valueChanged[int].connect(self._select_output_image)
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
            with input_context(self.get_task_output_value("imagestacks")) as images:
                binit = False
                yield images
        except TypeError:
            if binit:
                yield list()

    def _update_output_data(self):
        with self._output_context() as images:
            self._slider.setMaximum(max(len(images) - 1, 0))
            if isinstance(images, InputStackNumpy):
                self._slider2.setMaximum(max(images.shape[1] - 1, 0))
            else:
                self._slider2.setMaximum(max(len(images) - 1, 0))
            self._select_output_image(self._slider2.value(), images=images)
            self._select_output_stack(self._slider.value(), images=images)

    def _select_output_image(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                self.current_image = select
                self._plot.addImage(
                    images[self.current_stack, select],
                    legend="image",
                )

    def _select_output_stack(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                name = self.get_task_output_value("stack_names")[select]
                self.current_stack = select
                self._plot.addImage(
                    images[select, self.current_image],
                    legend="image",
                    ylabel=" ",
                    xlabel=name,
                )
