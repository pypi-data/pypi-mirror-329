from contextlib import contextmanager

from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import SelectSlice
from ewoksndreg.io.input_stack import input_context


__all__ = ["OWSelectSlice"]


class OWSelectSlice(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=SelectSlice
):
    name = "Select Slice"
    description = "Manually select a slice of the volume, x,y,z have slice syntax"
    icon = "icons/select_slice.svg"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()
        self.shape = (0, 0, 0)

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        options = {
            "imagestack": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "url": {"value_for_type": ""},
            "x": {"value_for_type": ""},
            "y": {"value_for_type": ""},
            "z": {"value_for_type": ""},
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
        self._slider = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._slider)
        self._slider.valueChanged[int].connect(self._select_output_image)
        self._update_output_data()

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)
        self.draw_lines()

    @contextmanager
    def _output_context(self, images=None):
        if images is not None:
            yield images
            return
        try:
            binit = True
            with input_context(self.get_task_input_value("imagestack")) as images:
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
            if not images:
                return

            self._plot.addImage(images[select], legend="image")

    def draw_lines(self):
        x = self.get_task_input_value("x", f"0:{self.shape[2]}")
        y = self.get_task_input_value("y", f"0:{self.shape[1]}")
        x = slice(
            *map(lambda x: int(x.strip()) if x.strip() else None, x.split(":", 2))
        )
        y = slice(
            *map(lambda x: int(x.strip()) if x.strip() else None, y.split(":", 2))
        )
        self._plot.addCurve(
            [x.start, x.stop],
            [y.start, y.start],
            legend="x0",
            color="#FF0000",
            linestyle="-",
        )
        self._plot.addCurve(
            [x.start, x.stop],
            [y.stop, y.stop],
            legend="x1",
            color="#FF0000",
            linestyle="-",
        )
        self._plot.addCurve(
            [x.start, x.start],
            [y.start, y.stop],
            legend="y0",
            color="#FF0000",
            linestyle="-",
        )
        self._plot.addCurve(
            [x.stop, x.stop],
            [y.start, y.stop],
            legend="y1",
            color="#FF0000",
            linestyle="-",
        )
