import numpy
import pytest
from ..features.mapping.lstsq import get_lstsq_solver

try:
    from ..features.mapping.scikitimage_backend import get_ransac_solver
except ImportError:
    get_ransac_solver = None
from ..transformation.numpy_backend import homography_transform_coordinates

SOLVERS = {"lstsq": get_lstsq_solver, "ransac": get_ransac_solver}
OPTIONS = {"lstsq": dict(), "ransac": {"min_samples": 8, "residual_threshold": 2}}


@pytest.fixture
def random_state(scope="module"):
    return numpy.random.RandomState(seed=100)


@pytest.mark.parametrize("solver", list(SOLVERS))
def test_solver_translation(solver, random_state):
    func = SOLVERS[solver]
    if func is None:
        pytest.skip("dependencies not installed")
    options = OPTIONS[solver]

    from_coordinates = random_state.uniform(-10, 10, (2, 10))

    active = numpy.identity(3, dtype=numpy.float32)
    active[0:2, 2] = [1, 2]

    to_coordinates = homography_transform_coordinates(active, from_coordinates)
    active2 = func("translation", **options)(from_coordinates, to_coordinates)
    numpy.testing.assert_allclose(active, active2)


@pytest.mark.parametrize("solver", list(SOLVERS))
def test_solver_rigid(solver, random_state):
    func = SOLVERS[solver]
    if func is None:
        pytest.skip("dependencies not installed")
    options = OPTIONS[solver]

    from_coordinates = random_state.uniform(-10, 10, (2, 10))

    active = numpy.identity(3, dtype=numpy.float32)
    active[0:2, 2] = [1, 2]
    active[0, 0] = numpy.cos(0.1)
    active[1, 0] = numpy.sin(0.1)
    active[0, 1] = -numpy.sin(0.1)
    active[1, 1] = numpy.cos(0.1)

    to_coordinates = homography_transform_coordinates(active, from_coordinates)
    active2 = func("rigid", **options)(from_coordinates, to_coordinates)
    numpy.testing.assert_allclose(active, active2, rtol=1e-2)


@pytest.mark.parametrize("solver", list(SOLVERS))
def test_solver_similarity(solver, random_state):
    func = SOLVERS[solver]
    if func is None:
        pytest.skip("dependencies not installed")
    options = OPTIONS[solver]

    from_coordinates = random_state.uniform(-10, 10, (2, 10))

    active = numpy.identity(3, dtype=numpy.float32)
    active[0:2, 2] = [1, 2]
    active[0, 0] = 1.1 * numpy.cos(0.1)
    active[1, 0] = numpy.sin(0.1)
    active[0, 1] = -numpy.sin(0.1)
    active[1, 1] = 1.1 * numpy.cos(0.1)

    to_coordinates = homography_transform_coordinates(active, from_coordinates)
    active2 = func("similarity", **options)(from_coordinates, to_coordinates)
    numpy.testing.assert_allclose(active, active2)


@pytest.mark.parametrize("solver", list(SOLVERS))
def test_solver_affine(solver, random_state):
    func = SOLVERS[solver]
    if func is None:
        pytest.skip("dependencies not installed")
    options = OPTIONS[solver]

    from_coordinates = random_state.uniform(-10, 10, (2, 10))

    active = numpy.identity(3, dtype=numpy.float32)
    active[0:2, 2] = [1, 2]
    active[0, 0] = 1.1 * numpy.cos(0.1)
    active[1, 0] = numpy.sin(0.1)
    active[0, 1] = -numpy.sin(0.1)
    active[1, 1] = 1.2 * numpy.cos(0.1)

    to_coordinates = homography_transform_coordinates(active, from_coordinates)
    active2 = func("affine", **options)(from_coordinates, to_coordinates)
    numpy.testing.assert_allclose(active, active2)


@pytest.mark.parametrize("solver", list(SOLVERS))
def test_solver_projective(solver, random_state):
    func = SOLVERS[solver]
    if func is None:
        pytest.skip("dependencies not installed")
    options = OPTIONS[solver]

    from_coordinates = random_state.uniform(-10, 10, (2, 10))

    active = numpy.identity(3, dtype=numpy.float32)
    active[2, 0] = 0.2

    to_coordinates = homography_transform_coordinates(active, from_coordinates)
    active2 = func("projective", **options)(from_coordinates, to_coordinates)
    numpy.testing.assert_allclose(active, active2, atol=1e-10)
