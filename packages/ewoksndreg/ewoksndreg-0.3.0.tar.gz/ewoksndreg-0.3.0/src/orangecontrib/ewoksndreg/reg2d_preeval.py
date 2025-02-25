from contextlib import contextmanager

from silx.gui.plot import Plot2D
from silx.gui.colors import Colormap
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import Reg2DPreEvaluation
from ewoksndreg.io.input_stack import input_context, InputStack


__all__ = ["OWReg2DPreEvaluation"]


class OWReg2DPreEvaluation(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Reg2DPreEvaluation
):
    name = "Pre-Registration Evaluation"
    description = "Generate ranking of most promising stacks based on noisiness and peak in phase cross correlation"
    icon = "icons/reg2d_preeval.svg"

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
            "imagestacks": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "preferences": {"value_for_type": ""},
            "relevant_stacks": {"value_for_type": 0},
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
        self._stack_slider = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._stack_slider)
        self._stack_slider.valueChanged[int].connect(self._select_output_stack)
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
            with input_context(self.get_task_input_value("imagestacks")) as images:
                binit = False
                yield images
        except TypeError:
            if binit:
                yield list()

    def _update_output_data(self):
        with self._output_context() as images:
            self._stack_slider.setMaximum(max(len(images) - 1, 0))
            if isinstance(images, InputStack):
                self._slider.setMaximum(max(images.shape[1] - 1, 0))
            else:
                self._slider.setMaximum(max(len(images) - 1, 0))
            self._select_output_stack(self._stack_slider.value(), images=images)
            self._select_output_image(self._slider.value(), images=images)

    def _select_output_image(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                ranking = self.get_task_output_value("full_ranking")
                if ranking:
                    rank = ranking[self.current_stack]
                else:
                    rank = self.current_stack
                self.current_image = select
                self._plot.addImage(
                    images[rank, select],
                    legend="image",
                    colormap=Colormap(name="viridis"),
                )

    def _select_output_stack(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                ranking = self.get_task_output_value("full_ranking", None)
                if ranking is None:
                    rank = select
                else:
                    rank = ranking[select]
                name = self.get_task_input_value("stack_names", "")
                if name != "":
                    name = name[rank]
                self.current_stack = select
                self._plot.addImage(
                    images[rank, self.current_image],
                    legend="image",
                    ylabel=" ",
                    xlabel=name,
                    colormap=Colormap(name="viridis"),
                )
