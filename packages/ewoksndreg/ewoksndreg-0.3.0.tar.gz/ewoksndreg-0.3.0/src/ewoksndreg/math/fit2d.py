import warnings
import numpy

try:
    from scipy.optimize import leastsq
except ImportError:
    leastsq = None


def gaussian(x, y, x0, y0, sx, sy, rho, A):
    num = (
        (x - x0) ** 2 / sx**2
        - 2 * rho / (sx * sy) * (x - x0) * (y - y0)
        + (y - y0) ** 2 / sy**2
    )
    denom = 2 * (1 - rho**2)
    return (
        A / (2 * numpy.pi * sx * sy * numpy.sqrt(1 - rho**2)) * numpy.exp(-num / denom)
    )


def errorf_gaussian(p, x, y, data):
    x0, y0, sx, sy, rho, A = tuple(p)
    return numpy.ravel(gaussian(x, y, x0, y0, sx, sy, rho, A) - data)


def guess_gaussian(x, y, data):
    y0i, x0i = numpy.unravel_index(numpy.argmax(data), data.shape)
    y0 = y[y0i, 0]
    x0 = x[0, x0i]

    xv = x[y0i, :] - x0
    yv = data[y0i, :]
    sx = numpy.sqrt(abs(xv**2 * yv).sum() / yv.sum())
    xv = y[:, x0i] - y0
    yv = data[:, x0i]
    sy = numpy.sqrt(abs(xv**2 * yv).sum() / yv.sum())
    rho = 0.0

    A = data[y0, x0] * 2 * numpy.pi * sx * sy * numpy.sqrt(1 - rho**2)

    return numpy.array([x0, y0, sx, sy, rho, A], dtype=numpy.float32)


def fitgaussian(x, y, data):
    if leastsq is None:
        raise RuntimeError("requires 'scipy'")
    guess = guess_gaussian(x, y, data)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p, success = leastsq(errorf_gaussian, guess, args=(x, y, data))
        success = success > 0 and success < 5

    return p, success
