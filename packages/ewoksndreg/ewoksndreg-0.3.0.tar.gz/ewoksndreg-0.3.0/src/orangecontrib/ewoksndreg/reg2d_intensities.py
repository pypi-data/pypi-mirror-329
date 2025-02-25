from contextlib import contextmanager
from typing import Dict
from AnyQt import QtWidgets
import numpy as np

from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D, ComplexImageView
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser

from ewokscore import missing_data
from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksndreg.registry import RegistryId
from ewoksndreg.tasks import Reg2DIntensities
from ewoksndreg.intensities import registration
from ewoksndreg.intensities.types import (
    SitkMetricType,
    SitkOptimizerType,
    KorniaMetricType,
    KorniaOptimizerType,
)
from ewoksndreg.math.filter import FilterType, WindowType, preprocess
from ewoksndreg.math.fft import fft2, ifft2, fftshift
from ewoksndreg.transformation.types import TransformationType
from ewoksndreg.io.input_stack import input_context, InputStack


__all__ = ["OWReg2DIntensities"]


class OWReg2DIntensities(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=Reg2DIntensities
):
    name = "2D Intensity-Based Registration"
    description = "Calculate transformations of a stack of images based on intensities"
    icon = "icons/registration.png"

    _METHOD_OPTIONS = {
        "Numpy": {},
        "SimpleITK": {
            "metric": {
                "value_for_type": list(SitkMetricType.__members__),
                "serialize": str,
            },
            "optimizer": {
                "value_for_type": list(SitkOptimizerType.__members__),
                "serialize": str,
            },
            "pyramid_levels": {"value_for_type": 0},
            "order": {"value_for_type": 0},
            "sampling": {
                "value_for_type": ["none", "random", "regular"],
                "serialize": str,
            },
            "sampling%": {
                "value_for_type": 0.5,
                "serialize": str,
            },
        },
        "Kornia": {
            "metric": {
                "value_for_type": list(KorniaMetricType.__members__),
                "serialize": str,
            },
            "optimizer": {
                "value_for_type": list(KorniaOptimizerType.__members__),
                "serialize": str,
            },
            "pyramid_levels": {"value_for_type": 0},
        },
        "SciKitImage": {
            "normalized": {"value_for_type": False},
            "upsample_factor": {"value_for_type": 0},
            "sim_normalized": {"value_for_type": False},
            "sim_upsample_factor": {"value_for_type": 0},
        },
    }

    _PREPROC_OPTIONS = {
        "apply_filter": {
            "value_for_type": list(FilterType.__members__),
            "serialize": str,
        },
        "filter_parameter": {"value_for_type": 0.1},
        "apply_low_pass": {"value_for_type": 0.1},
        "apply_high_pass": {"value_for_type": 0.1},
        "pin_range": {"value_for_type": False},
        "apply_window": {
            "value_for_type": list(WindowType.__members__),
            "serialize": str,
        },
    }

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)
        proper_transformations = list(TransformationType.__members__)
        try:
            proper_transformations.remove("composite")
            proper_transformations.remove("identity")
        except ValueError:
            pass
        options = {
            "imagestack": {"value_for_type": "", "select": "h5dataset"},
            "inputs_are_stacks": {"value_for_type": False},
            "transformation_type": {
                "value_for_type": proper_transformations,
                "serialize": str,
            },
            "reference": {"value_for_type": 0},
            "block_size": {"value_for_type": 1},
        }

        for name, kw in options.items():
            self._default_inputs_form.addParameter(
                name,
                value=values[name],
                value_change_callback=self._default_inputs_changed,
                **kw,
            )
        self._default_inputs_form.addParameter(
            "mapper",
            value=values["mapper"],
            value_for_type=registration.IntensityMapping.get_subclass_ids(),
            serialize=str,
            value_change_callback=self._mapper_changed,
        )

        layout = self._get_control_layout()
        self._tabs = QtWidgets.QTabWidget(parent=self.controlArea)
        layout.addWidget(self._tabs)

        # preprocessing tab
        self._prep_widget = QtWidgets.QWidget(parent=self.controlArea)
        layout = QtWidgets.QVBoxLayout()
        self._prep_widget.setLayout(layout)
        self._prepform = ParameterForm(parent=self.controlArea)
        for name, kw in self._PREPROC_OPTIONS.items():
            self._prepform.addParameter(
                name,
                value_change_callback=self._preproc_inputs_changed,
                **kw,
            )
        if values["preprocessing_options"]:
            self._prepform.set_parameter_values(values["preprocessing_options"])
        layout.addWidget(self._prepform)
        self._tabs.addTab(self._prep_widget, "Preprocessing")

        # tabs for each of the backends
        self._pforms: Dict[str, ParameterForm] = {}
        self._tab_widgets: Dict[str, QtWidgets.QWidget] = {}
        for mapper in registration.IntensityMapping.get_subclass_ids():
            options = [
                self._METHOD_OPTIONS[key]
                for key in self._METHOD_OPTIONS.keys()
                if key in str(mapper)
            ][0]

            w = QtWidgets.QWidget(parent=self.controlArea)
            layout = QtWidgets.QVBoxLayout()
            w.setLayout(layout)
            self._pforms[str(mapper)] = ParameterForm(parent=w)
            for name, kw in options.items():
                self._pforms[str(mapper)].addParameter(
                    name,
                    value_change_callback=self._other_inputs_changed,
                    **kw,
                )
            layout.addWidget(self._pforms[str(mapper)])
            self._tabs.addTab(w, mapper.backend)
            self._tab_widgets[str(mapper)] = w
        if values["mapper"] and values["method_options"]:
            self._pforms[values["mapper"]].set_parameter_values(
                values["method_options"]
            )

    def _default_inputs_changed(self):
        self.update_default_inputs(**self._default_inputs_form.get_parameter_values())
        self._update_data()

    def _preproc_inputs_changed(self):
        kw = {
            key: item
            for key, item in self._prepform.get_parameter_values().items()
            if not missing_data.is_missing_data(item)
        }
        self.update_default_inputs(preprocessing_options=kw)
        self._add_image(self._vtab.currentIndex(), None)

    def _other_inputs_changed(self):
        current_mapper = self._default_inputs_form.get_parameter_value("mapper")
        if current_mapper:
            method_options = self._pforms[current_mapper].get_parameter_values()
            kw = {
                key: item
                for key, item in method_options.items()
                if not missing_data.is_missing_data(item)
            }
            self.update_default_inputs(method_options=kw)
        self._update_data()

    def _mapper_changed(self):
        self.update_default_inputs(**self._default_inputs_form.get_parameter_values())
        mapper = self.get_task_input_value("mapper", None)
        if mapper is None:
            self._tabs.setCurrentWidget(self._prep_widget)
            self._update_data()
            return
        self._update_transfo_types(RegistryId.factory(mapper))
        self._tabs.setCurrentWidget(self._tab_widgets[mapper])
        method_options = self._pforms[mapper].get_parameter_values()
        kw = {
            key: item
            for key, item in method_options.items()
            if not missing_data.is_missing_data(item)
        }
        self.update_default_inputs(method_options=kw)

    def _update_transfo_types(self, mapper: RegistryId):
        cls = registration.IntensityMapping.get_subclass(mapper)
        current_type = str(self.get_task_input_value("transformation_type"))
        allowed_types = cls.SUPPORTED_TRANSFORMATIONS
        transfo_widg = self._default_inputs_form._get_value_widget(
            "transformation_type"
        )
        transfo_widg.clear()
        transfo_widg.addItem("<missing>", missing_data.MISSING_DATA)
        for _type in allowed_types:
            transfo_widg.addItem(str(_type), str(_type))
        if current_type in allowed_types:
            transfo_widg.setCurrentText(current_type)
            self.update_default_inputs(transformation_type=current_type)

    def handleNewSignals(self) -> None:
        self._update_input_data()
        self._update_data()
        super().handleNewSignals()

    def task_output_changed(self):
        self._update_data()

    def _init_main_area(self):
        super()._init_main_area()
        layout = self._get_main_layout()

        self._vtab = QtWidgets.QTabWidget(parent=self.mainArea)

        layout.addWidget(self._vtab)

        self._main_visual = QtWidgets.QWidget(parent=self.mainArea)
        tab_layout = QtWidgets.QVBoxLayout()
        self._main_visual.setLayout(tab_layout)
        self._plot = Plot2D(parent=self._main_visual)
        self._plot.setDefaultColormap(Colormap("viridis"))
        tab_layout.addWidget(self._plot)
        self._vtab.addTab(self._main_visual, "Images")
        self._plot.getMaskToolsDockWidget().sigMaskChanged.connect(self._mask_changed)

        self._fft_visual = QtWidgets.QWidget(parent=self.mainArea)
        tab_layout = QtWidgets.QVBoxLayout()
        self._fft_visual.setLayout(tab_layout)
        self._fftplot = ComplexImageView.ComplexImageView(parent=self._fft_visual)
        self._fftplot.setColormap(Colormap("viridis", normalization=Colormap.LOGARITHM))
        tab_layout.addWidget(self._fftplot)
        self._vtab.addTab(self._fft_visual, "Fourier")

        self._fftprod_visual = QtWidgets.QWidget(parent=self.mainArea)
        tab_layout = QtWidgets.QVBoxLayout()
        self._fftprod_visual.setLayout(tab_layout)
        self._fftprodplot = ComplexImageView.ComplexImageView(
            parent=self._fftprod_visual
        )
        self._fftprodplot.setColormap(Colormap("viridis"))
        tab_layout.addWidget(self._fftprodplot)
        self._vtab.addTab(self._fftprod_visual, "Cross-correlogram")

        self.current_stack = 0
        self.current_image = 0
        self._vtab.currentChanged[int].connect(self._add_image)

        self._stack_slider = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._stack_slider)
        self._stack_slider.valueChanged[int].connect(self._select_stack)
        self._img_slider = HorizontalSliderWithBrowser(parent=self.mainArea)
        layout.addWidget(self._img_slider)
        self._img_slider.valueChanged[int].connect(self._select_image)
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
                yield [
                    [],
                ]

    def _update_data(self):
        with self._input_context() as images:
            if isinstance(images, InputStack):
                if images.ndim == 3:
                    self._stack_slider.hide()
                    self._img_slider.setMaximum(max(len(images) - 1, 0))
                else:
                    self._stack_slider.show()
                    self._stack_slider.setMaximum(max(len(images) - 1, 0))
                    self._img_slider.setMaximum(max(len(images[0]) - 1, 0))
            self._select_stack(self._stack_slider.value(), images=images)
            self._select_image(self._img_slider.value(), images=images)

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

    def _select_image(self, select, images=None):
        self.current_image = select
        self._add_image(self._vtab.currentIndex(), images)

    def _select_stack(self, select, images=None):
        self.current_stack = select
        self._add_image(self._vtab.currentIndex(), images)

    def _add_image(self, tab, images=None):
        with self._input_context(images=images) as images:
            if not isinstance(images, InputStack):
                return
            preprocessing_options = self.get_task_input_value(
                "preprocessing_options", {}
            )
            if images.ndim == 3:
                image = preprocess(images[self.current_image], **preprocessing_options)
            elif images.ndim == 4:
                image = preprocess(
                    images[self.current_stack, self.current_image],
                    **preprocessing_options,
                )
            if tab == 0:
                self._plot.addImage(image, legend="image")
            elif tab == 1:
                self._fftplot.setData(fft2(image, centered=True), False)
            elif tab == 2:
                reference = self.get_task_input_value("reference", 0)
                if images.ndim == 3:
                    if reference == -1:
                        reference = len(images) // 2
                    ref = preprocess(images[reference], **preprocessing_options)
                elif images.ndim == 4:
                    if reference == -1:
                        reference = images.shape[1] // 2
                    ref = preprocess(
                        images[self.current_stack, reference], **preprocessing_options
                    )
                prod = fft2(image) * fft2(ref).conj()
                pcc = ifft2(prod / np.abs(prod))
                self._fftprodplot.setData(fftshift(pcc), False)

    def _mask_changed(self):
        mask = self._plot.getSelectionMask()
        if mask.ndim == 2:
            if np.any(mask):
                self.update_default_inputs(mask=mask)
            else:
                self.update_default_inputs(mask=missing_data.MISSING_DATA)
            self._default_inputs_changed()
