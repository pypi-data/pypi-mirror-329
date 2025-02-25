import sys
from numbers import Integral
from typing import Tuple, Sequence, Union, Optional, Iterator
from contextlib import contextmanager
from collections.abc import Sequence as AbsSequence

import numpy
from numpy.typing import DTypeLike

from silx.io import h5py_utils
from silx.io.url import DataUrl


class InputStack(AbsSequence):
    def __enter__(self) -> "InputStack":
        return self

    def __exit__(self, *args) -> None:
        pass

    def __getitem__(self, idx) -> numpy.ndarray:
        raise NotImplementedError

    @property
    def shape(self) -> Tuple[int]:
        raise NotImplementedError

    @property
    def dtype(self) -> DTypeLike:
        raise NotImplementedError

    def __len__(self) -> int:
        return self.shape[0]

    @property
    def ndim(self) -> int:
        return len(self.shape)


class InputStackNumpy(InputStack):
    def __init__(
        self,
        arrays: Union[numpy.ndarray, Sequence[numpy.ndarray]],
        inputs_are_stacks: Optional[bool] = None,
    ) -> None:
        if isinstance(arrays, numpy.ndarray):
            if inputs_are_stacks is None:
                inputs_are_stacks = True
            if not inputs_are_stacks:
                arrays = arrays[None, ...]
            self._array = arrays
        elif isinstance(arrays, Sequence):
            if inputs_are_stacks is None:
                inputs_are_stacks = False
            if inputs_are_stacks:
                self._array = numpy.vstack(arrays)
            else:
                self._array = numpy.stack(arrays, axis=0)
        else:
            raise TypeError("arrays")
        super().__init__()

    def __getitem__(self, idx) -> numpy.ndarray:
        return self._array[idx]

    @property
    def shape(self) -> Tuple[int]:
        return self._array.shape

    @property
    def dtype(self) -> DTypeLike:
        return self._array.dtype


class InputStackHdf5(InputStack):
    def __init__(
        self, uris: Union[str, Sequence[str]], inputs_are_stacks: Optional[bool] = None
    ) -> None:
        if isinstance(uris, str):
            self._uris = [DataUrl(uris)]
            if inputs_are_stacks is None:
                inputs_are_stacks = True
        else:
            self._uris = [DataUrl(s) for s in uris]
            if inputs_are_stacks is None:
                inputs_are_stacks = False
        self._uris_are_stacks = inputs_are_stacks
        self._clean_resources()
        super().__init__()

    def __enter__(self) -> "InputStackHdf5":
        self._clean_resources()
        try:
            for uri in self._uris:
                ctx = h5py_utils.File(uri.file_path())
                self._file_objs.append(ctx.__enter__())
        except BaseException:
            for ctx in self._file_objs:
                ctx.__exit__(*sys.exc_info())
            raise
        return super().__enter__()

    def __exit__(self, *args) -> None:
        for ctx in self._file_objs:
            ctx.__exit__(*args)
        self._clean_resources()

    def _clean_resources(self):
        self._file_objs = list()
        self._dset_objs = list()
        self._cumlen_uris = list()
        self._shape = None
        self._dtype = None

    def __getitem__(self, idx) -> numpy.ndarray:
        if not self._dset_objs:
            self._get_dset_info()

        if isinstance(idx, Tuple):
            idx0 = idx[0]
            idxrest = idx[1:]
        else:
            idx0 = idx
            idxrest = tuple()

        dim0scalar = False
        n = len(self)
        if isinstance(idx0, Integral):
            idx0 = numpy.asarray([idx0])
            dim0scalar = True
        elif isinstance(idx0, slice):
            idx0 = numpy.array(range(*idx0.indices(n)))
        elif isinstance(idx0, Sequence):
            idx0 = numpy.asarray(idx0)
        elif idx0 is Ellipsis:
            idx0 = numpy.array(range(n))
        else:
            raise TypeError

        result = list()
        for i in idx0:
            while i < 0:
                i += n
            dseti = numpy.where(self._cumlen_uris > i)[0][0]
            dset = self._dset_objs[dseti]
            if self._uris_are_stacks:
                if dseti > 0:
                    i -= self._cumlen_uris[dseti - 1]
                idxdset = (i,) + idxrest
            else:
                idxdset = idxrest
            result.append(dset[idxdset])

        if dim0scalar:
            return result[0]
        else:
            return numpy.array(result)

    @property
    def shape(self) -> Tuple[int]:
        if self._shape is None:
            self._get_dset_info()
        return self._shape

    @property
    def dtype(self) -> DTypeLike:
        if self._dtype is None:
            self._get_dset_info()
        return self._dtype

    def _get_dset_info(self):
        if len(self._file_objs) != len(self._uris):
            raise RuntimeError("enter the context first")
        len_uris = list()
        dset_objs = list()
        ndim = set()
        shape = set()
        dtype = set()
        for uri, file_obj in zip(self._uris, self._file_objs):
            dset = file_obj[uri.data_path()]
            if self._uris_are_stacks:
                dset_ndim = dset.ndim
                dset_shape = dset.shape[1:]
                dset_len = len(dset)
            else:
                dset_ndim = dset.ndim + 1
                dset_shape = dset.shape
                dset_len = 1

            ndim.add(dset_ndim)
            if len(ndim) != 1:
                raise ValueError("array dimensions do not match")
            shape.add(dset_shape)
            if len(shape) != 1:
                raise ValueError("array dimensions do not match")
            dtype.add(dset.dtype)
            if len(dtype) != 1:
                raise ValueError("array dtype must be the same")
            len_uris.append(dset_len)
            dset_objs.append(dset)
        self._cumlen_uris = numpy.cumsum(len_uris, dtype=int)
        self._shape = (self._cumlen_uris[-1],) + next(iter(shape))
        self._dtype = next(iter(dtype))
        self._dset_objs = dset_objs


@contextmanager
def input_context(
    images, inputs_are_stacks: Optional[bool] = None
) -> Iterator[InputStack]:
    if isinstance(images, str) or (
        isinstance(images, Sequence) and isinstance(images[0], str)
    ):
        with InputStackHdf5(images, inputs_are_stacks=inputs_are_stacks) as stack:
            yield stack
    else:
        with InputStackNumpy(images, inputs_are_stacks=inputs_are_stacks) as stack:
            yield stack
