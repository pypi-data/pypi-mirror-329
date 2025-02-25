import numpy
from ...math import fit2d


def test_leastsq():
    nx = 501
    ny = 401
    y, x = numpy.indices((ny, nx))
    x0 = 10
    y0 = ny // 2
    sx = nx // 4
    sy = ny // 4
    rho = 0.5
    A = 1000.0
    p1 = numpy.array([x0, y0, sx, sy, rho, A], dtype=numpy.float32)
    x0, y0, sx, sy, rho, A = tuple(p1)

    data = fit2d.gaussian(x, y, x0, y0, sx, sy, rho, A)

    p2, _ = fit2d.fitgaussian(x, y, data)
    numpy.testing.assert_allclose(p1, p2)
