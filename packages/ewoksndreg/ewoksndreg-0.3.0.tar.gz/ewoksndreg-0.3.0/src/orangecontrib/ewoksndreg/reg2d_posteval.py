from contextlib import contextmanager

from silx.gui.plot import Plot2D
from silx.gui.colors import Colormap
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from AnyQt.QtWidgets import QTabWidget, QWidget, QVBoxLayout

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import Reg2DPostEvaluation
from ewoksndreg.io.input_stack import input_context, InputStack


__all__ = ["OWReg2DPostEvaluation"]


class OWReg2DPostEvaluation(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Reg2DPostEvaluation
):
    name = "Post-Registration Evaluation"
    description = "Choose the best registration based on the calculated transformations for each stack"
    icon = "icons/reg2d_posteval.png"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()
        self.current_image = 0
        self.current_stack = 0

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)
        options = {
            "imagestacks": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "chosen_stack": {"value_for_type": -1},
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
        self._tabs = QTabWidget(parent=self.mainArea)
        layout.addWidget(self._tabs)

        w = QWidget(parent=self.mainArea)
        layout = QVBoxLayout()
        w.setLayout(layout)
        self.cplot = Plot2D(parent=w)
        self._cslider = HorizontalSliderWithBrowser(parent=w)
        layout.addWidget(self.cplot)
        layout.addWidget(self._cslider)
        self._tabs.addTab(w, "Choice")

        w = QWidget(parent=self.mainArea)
        layout = QVBoxLayout()
        w.setLayout(layout)
        self.allplot = Plot2D(parent=w)
        self._stackslider = HorizontalSliderWithBrowser(parent=w)
        self._slider = HorizontalSliderWithBrowser(parent=w)
        layout.addWidget(self.allplot)
        layout.addWidget(self._stackslider)
        layout.addWidget(self._slider)
        self._tabs.addTab(w, "All Options")

        self._stackslider.valueChanged[int].connect(self._select_stack)
        self._slider.valueChanged[int].connect(self._select_image)
        self._cslider.valueChanged[int].connect(self._select_choice_image)

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

    @contextmanager
    def _output_context(self, imagestacks=None):
        if imagestacks is not None:
            yield imagestacks
            return
        try:
            binit = True
            with input_context(
                self.get_task_output_value("imagestacks")
            ) as imagestacks:
                binit = False
                yield imagestacks
        except TypeError:
            if binit:
                yield list()

    @contextmanager
    def _choice_context(self, images=None):
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
        with self._output_context() as imagestacks:
            self._stackslider.setMaximum(max(len(imagestacks) - 1, 0))
            if isinstance(imagestacks, InputStack):
                self._slider.setMaximum(max(imagestacks.shape[1] - 1, 0))
            else:
                self._slider.setMaximum(max(len(imagestacks) - 1, 0))

            self._select_stack(self._stackslider.value(), images=imagestacks)
            self._select_image(self._slider.value(), images=imagestacks)

        with self._choice_context() as images:
            self._cslider.setMaximum(max(len(images) - 1, 0))
            self._select_choice_image(self._cslider.value(), images=images)

    def _select_stack(self, select, images=None):
        with self._output_context(imagestacks=images) as images:
            if images:
                self.current_stack = select
                self.allplot.addImage(
                    images[select, self.current_image],
                    legend="image",
                    colormap=Colormap(name="viridis"),
                )

    def _select_image(self, select, images=None):
        with self._output_context(imagestacks=images) as images:
            if images:
                self.current_image = select
                self.allplot.addImage(
                    images[self.current_stack, select],
                    legend="image",
                    colormap=Colormap(name="viridis"),
                )

    def _select_choice_image(self, select, images=None):
        with self._choice_context(images=images) as images:
            if images:
                self.cplot.addImage(
                    images[select],
                    legend="image",
                    colormap=Colormap(name="viridis"),
                )
