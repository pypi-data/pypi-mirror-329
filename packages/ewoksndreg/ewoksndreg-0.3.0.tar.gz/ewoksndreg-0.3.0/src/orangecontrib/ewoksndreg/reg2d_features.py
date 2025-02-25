from contextlib import contextmanager
import numpy

from silx.gui.plot import Plot2D
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.tasks import Reg2DFeatures
from ewoksndreg.features import registration
from ewoksndreg.transformation.types import TransformationType
from ewoksndreg.io.input_stack import input_context


__all__ = ["OWReg2DFeatures"]


class OWReg2DFeatures(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Reg2DFeatures
):
    name = "2D Feature-Based Registration"
    description = "Calculate transformations of a stack of images based on features"
    icon = "icons/2d_features.svg"

    def __init__(self):
        super().__init__()
        self._space = 0.05
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        options = {
            "imagestack": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "reference": {"value_for_type": 0},
            "transformation_type": {
                "value_for_type": list(TransformationType.__members__),
                "serialize": str,
            },
            "detector": {
                "value_for_type": registration.FeatureDetector.get_subclass_ids(),
                "serialize": str,
            },
            "matcher": {
                "value_for_type": registration.FeatureMatching.get_subclass_ids(),
                "serialize": str,
            },
            "mapper": {
                "value_for_type": registration.FeatureMapping.get_subclass_ids(),
                "serialize": str,
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
        self._update_data()

    def handleNewSignals(self) -> None:
        self._update_input_data()
        super().handleNewSignals()

    def task_output_changed(self):
        self._update_data()

    def _init_main_area(self):
        super()._init_main_area()
        layout = self._get_main_layout()
        self._plot = Plot2D(parent=self.mainArea)
        layout.addWidget(self._plot)
        self._slider = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._slider)
        self._slider.valueChanged[int].connect(self._select_image)
        self._update_data()

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

    def _update_data(self):
        with self._input_context() as images:
            self._slider.setMaximum(max(len(images) - 1, 0))
            self._select_image(self._slider.value(), images=images)

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

    def _select_image(self, select, images=None):
        with self._input_context(images=images) as images:
            if not images:
                return
            reference = self.get_task_input_value("reference", 0)
            refimg = images[reference]
            selimg = images[select]

            space = max(int(refimg.shape[1] * self._space), 1)
            spaceimg = numpy.full((refimg.shape[0], space), numpy.nan)
            off = refimg.shape[1] + space

            self._plot.addImage(
                numpy.hstack([refimg, spaceimg, selimg]), legend="images"
            )

            transformations = self.get_task_output_value("transformations")
            if not transformations:
                return
            features = self.get_task_output_value("features")
            matches = self.get_task_output_value("matches")

            def legend_generator():
                i = 0
                while True:
                    yield f"c{i}"
                    i += 1

            legend = legend_generator()

            self._plot.remove(kind="curve")

            yref, xref = features[reference].coordinates
            ysel, xsel = features[select].coordinates
            xsel = xsel + off

            self._plot.addCurve(
                xref,
                yref,
                legend=next(legend),
                symbol="+",
                linestyle=" ",
                color="#00FF00",
            )
            self._plot.addCurve(
                xsel,
                ysel,
                legend=next(legend),
                symbol="+",
                linestyle=" ",
                color="#00FF00",
            )

            reffeatures, selfeatures = matches[select]
            if reffeatures is None:
                reffeatures = features[reference]
                selfeatures = reffeatures
            yref, xref = reffeatures.coordinates
            ysel, xsel = selfeatures.coordinates
            xsel = xsel + off

            for x0, y0, x1, y1 in zip(xref, yref, xsel, ysel):
                self._plot.addCurve(
                    [x0, x1],
                    [y0, y1],
                    legend=next(legend),
                    color="#FF0000",
                    linestyle="-",
                )
