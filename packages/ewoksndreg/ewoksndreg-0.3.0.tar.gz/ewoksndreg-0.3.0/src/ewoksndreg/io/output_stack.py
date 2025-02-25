from typing import Optional, Iterator, List
from contextlib import contextmanager
from numpy.typing import ArrayLike

from silx.io import h5py_utils
from silx.io.url import DataUrl
from ewoksdata.data.hdf5.dataset_writer import DatasetWriter


class OutputStack:
    def __enter__(self) -> "OutputStack":
        return self

    def __exit__(self, *args) -> None:
        pass

    def add_point(self, data: ArrayLike) -> bool:
        raise NotImplementedError

    def add_points(self, data: ArrayLike) -> bool:
        raise NotImplementedError


class OutputStackNumpy(OutputStack):
    def __init__(self, data: list) -> None:
        self._data = data
        super().__init__()

    @property
    def data(self) -> List[ArrayLike]:
        return self._data

    def add_point(self, data: ArrayLike) -> bool:
        self._data.append(data)

    def add_points(self, data: ArrayLike) -> bool:
        self._data.extend(data)


class OutputStackHdf5(OutputStack):
    def __init__(self, uri: str) -> None:
        self._file_obj = None
        self._writer = None
        self._uri = DataUrl(uri)
        super().__init__()

    def __enter__(self) -> "OutputStackHdf5":
        ctx = h5py_utils.File(self._uri.file_path(), mode="a")
        self._file_obj = ctx.__enter__()

        data_path = self._uri.data_path()
        parent = self._file_obj
        names = [s for s in data_path.split("/") if s]
        if not names:
            raise ValueError("URL needs a data path")
        for name in names[:-1]:
            if not name:
                continue
            parent = parent.require_group(name)

        self._writer = DatasetWriter(parent, names[-1])
        return super().__enter__()

    def __exit__(self, *args) -> None:
        self._writer.flush_buffer()
        self._file_obj.__exit__(*args)
        self._file_obj = None
        self._writer = None
        return super().__exit__(*args)

    def add_point(self, data: ArrayLike) -> bool:
        if self._writer is None:
            raise RuntimeError("enter the context first")
        self._writer.add_point(data)

    def add_points(self, data: ArrayLike) -> bool:
        if self._writer is None:
            raise RuntimeError("enter the context first")
        self._writer.add_points(data)


@contextmanager
def output_context(url: Optional[str] = None) -> Iterator[OutputStack]:
    if url:
        with OutputStackHdf5(url) as stack:
            yield stack
    else:
        data = list()
        with OutputStackNumpy(data) as stack:
            yield stack
