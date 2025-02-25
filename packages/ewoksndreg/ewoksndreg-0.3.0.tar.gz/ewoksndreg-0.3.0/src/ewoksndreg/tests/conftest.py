import pytest
from ewoksorange.tests.conftest import qtapp  # noqa F401
from ewoksorange.canvas.handler import OrangeCanvasHandler


@pytest.fixture(scope="session")
def ewoks_orange_canvas(qtapp):  # noqa F811
    with OrangeCanvasHandler() as handler:
        yield handler
