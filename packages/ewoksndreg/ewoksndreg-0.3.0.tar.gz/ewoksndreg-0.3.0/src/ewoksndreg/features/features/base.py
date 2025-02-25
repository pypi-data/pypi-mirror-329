from typing import Optional, Type, Callable
from collections.abc import Sequence as AbcSequence
import numpy
from ...registry import Registered


class Features(AbcSequence, Registered, register=False):
    _FEATURE_TYPE_CONVERTERS = dict()

    @classmethod
    def _set_feature_type_converter(
        cls, to_cls: Type["Features"], converter: Callable[["Features"], "Features"]
    ):
        cls._FEATURE_TYPE_CONVERTERS[(cls, to_cls)] = converter

    @classmethod
    def _get_feature_type_converter(
        cls, to_cls: Type["Features"]
    ) -> Optional[Callable[["Features"], "Features"]]:
        return cls._FEATURE_TYPE_CONVERTERS.get((cls, to_cls))

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__(**kw)
        cls._set_feature_type_converter(cls, lambda x: x)

    def as_type(self, cls: Type["Features"]) -> "Features":
        func = self._get_feature_type_converter(cls)
        if func is not None:
            return func(self)
        raise TypeError(f"cannot convert '{type(self).__name__}' to '{cls.__name__}'")

    @property
    def coordinates(self) -> numpy.ndarray:
        # ndim x nfeatures
        raise NotImplementedError

    @property
    def ndim(self) -> int:
        raise NotImplementedError

    @property
    def nfeatures(self) -> int:
        raise NotImplementedError

    def __len__(self) -> int:
        return self.nfeatures

    def __getitem__(self, idx):
        raise NotImplementedError
