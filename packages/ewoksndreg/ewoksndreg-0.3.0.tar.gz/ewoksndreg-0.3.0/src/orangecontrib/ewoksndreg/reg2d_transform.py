from contextlib import contextmanager
from AnyQt import QtWidgets

from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import Reg2DTransform
from ewoksndreg.io.input_stack import input_context, InputStack

__all__ = ["OWReg2DTransform"]


class OWReg2DTransform(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Reg2DTransform
):
    name = "2D Transformation"
    description = "Apply image transformations to a stack of images"
    icon = "icons/transformation.png"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(
            include_missing=True, defaults={"interpolation_order": 1}
        )

        options = {
            "imagestack": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "url": {"value_for_type": ""},
            "interpolation_order": {"value_for_type": 0},
            "crop": {"value_for_type": False},
        }

        for name, kw in options.items():
            if name not in options:
                continue
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

        self._tabs = QtWidgets.QTabWidget(parent=self.mainArea)
        layout.addWidget(self._tabs)

        w = QtWidgets.QWidget(parent=self.mainArea)
        layout = QtWidgets.QVBoxLayout()
        w.setLayout(layout)
        self._oplot = Plot2D(parent=w)
        self._oplot.setDefaultColormap(Colormap("viridis"))
        self._oslider1 = HorizontalSliderWithBrowser(parent=w)
        self.current_in_stack = 0
        self._oslider2 = HorizontalSliderWithBrowser(parent=w)
        self.current_in_image = 0
        layout.addWidget(self._oplot)
        layout.addWidget(self._oslider1)
        layout.addWidget(self._oslider2)
        self._tabs.addTab(w, "Aligned")

        w = QtWidgets.QWidget(parent=self.mainArea)
        layout = QtWidgets.QVBoxLayout()
        w.setLayout(layout)
        self._iplot = Plot2D(parent=w)
        self._iplot.setDefaultColormap(Colormap("viridis"))
        self._islider1 = HorizontalSliderWithBrowser(parent=w)
        self.current_out_stack = 0
        self._islider2 = HorizontalSliderWithBrowser(parent=w)
        self.current_out_image = 0
        layout.addWidget(self._iplot)
        layout.addWidget(self._islider1)
        layout.addWidget(self._islider2)
        self._tabs.addTab(w, "Original")

        self._islider1.valueChanged[int].connect(self._select_in_stack)
        self._islider2.valueChanged[int].connect(self._select_in_image)
        self._oslider1.valueChanged[int].connect(self._select_out_stack)
        self._oslider2.valueChanged[int].connect(self._select_out_image)
        self._update_input_data()

    @contextmanager
    def _input_context(self, images=None):
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

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

        with self._input_context() as images:
            if isinstance(images, InputStack):
                if images.ndim == 3:
                    self._islider1.hide()
                    self._islider2.setMaximum(max(len(images) - 1, 0))
                else:
                    self._islider1.show()
                    self._islider1.setMaximum(max(len(images) - 1, 0))
                    self._islider2.setMaximum(max(len(images[0]) - 1, 0))
            self._select_in_stack(self._islider1.value(), images=images)
            self._select_in_image(self._islider2.value(), images=images)

    def _select_in_stack(self, select, images=None):
        self.current_in_stack = select
        self._select_in_image(self.current_in_image, images)

    def _select_in_image(self, select, images=None):
        with self._input_context(images=images) as images:
            if images:
                self.current_in_image = select
                if images.ndim == 3:
                    self._iplot.addImage(images[select], legend="image")
                else:
                    self._iplot.addImage(
                        images[self.current_in_stack, select], legend="image"
                    )

    def _update_output_data(self):
        with self._output_context() as images:
            if isinstance(images, InputStack):
                if images.ndim == 3:
                    self._oslider1.hide()
                    self._oslider2.setMaximum(max(len(images) - 1, 0))
                else:
                    self._oslider1.show()
                    self._oslider1.setMaximum(max(len(images) - 1, 0))
                    self._oslider2.setMaximum(max(len(images[0]) - 1, 0))
            self._select_out_stack(self._oslider1.value(), images=images)
            self._select_out_image(self._oslider2.value(), images=images)

    def _select_output_image(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                self._oplot.addImage(images[select], legend="image")

    def _select_out_stack(self, select, images=None):
        self.current_out_stack = select
        self._select_out_image(self.current_out_image, images)

    def _select_out_image(self, select, images=None):
        with self._output_context(images=images) as images:
            if images:
                self.current_out_image = select
                if images.ndim == 3:
                    self._oplot.addImage(images[select], legend="image")
                else:
                    self._oplot.addImage(
                        images[self.current_out_stack, select], legend="image"
                    )
