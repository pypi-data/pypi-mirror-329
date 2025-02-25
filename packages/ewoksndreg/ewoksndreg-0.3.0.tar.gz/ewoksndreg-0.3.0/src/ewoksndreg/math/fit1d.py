import warnings
import numpy

try:
    from scipy.optimize import leastsq as _leastsq
    from scipy.optimize import nnls
    from scipy.optimize import lsq_linear
except ImportError:
    _leastsq = None
    nnls = None
    lsq_linear = None


def gaussian(x, x0, sx, A):
    return (
        A / (numpy.sqrt(2 * numpy.pi) * sx) * numpy.exp(-((x - x0) ** 2) / (2 * sx**2))
    )


def guess_gaussian(x, data):
    x0i = numpy.argmax(data)
    x0 = x[x0i]
    sx = numpy.sqrt(abs((x - x0) ** 2 * data).sum() / data.sum())
    A = data[x0] * numpy.sqrt(2 * numpy.pi) * sx
    return numpy.array([x0, sx, A], dtype=numpy.float32)


def fitgaussian(x, data):
    return leastsq(x, data, guessfunc=guess_gaussian, fitfunc=gaussian)


def leastsq(x, data, guessfunc=None, fitfunc=None):
    if _leastsq is None:
        raise RuntimeError("requires 'scipy'")
    guess = guessfunc(x, data)

    def errorfunc(p, x, data):
        return numpy.ravel(fitfunc(x, *p) - data)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p, success = _leastsq(errorfunc, guess, args=(x, data))
        success = success > 0 and success < 5

    return p, success


def xyremovenan(x, y):
    b = numpy.logical_and(~numpy.isnan(x), ~numpy.isnan(y))
    return x[b], y[b]


def cor_from_cov(cov):
    D = numpy.diag(1 / numpy.sqrt(numpy.diag(cov)))
    return D.dot(cov.dot(D))


def lstsq_cov(A, vare=None, cove=None):
    """Covariance matrix of the least squares solution
    of a linear system.

    .. math::

        A.x = b + e

        E(e) = 0

    Args:
        A(array): (m x n)
        vare(array): variance on e (m)
        cove(array): covariance matrix of e (m x m)

    Returns:
        covx(array): (n x n)
    """
    # A.x = b + e
    # E(e) = 0
    #
    # Least squares estimator of x:
    #  x = M.b
    #  M = (A^T.A)^(-1).A^T
    #  COV(x) = M.COV(e).M^T
    # https://stat.ethz.ch/~geer/bsa199_o.pdf

    m, n = A.shape
    if m == n:
        try:
            # M = A^(-1)
            if cove is None:
                return numpy.linalg.inv(A.T.dot(A / vare.reshape((m, 1))))
            else:
                iA = numpy.linalg.inv(A)
                return iA.dot(cove.dot(iA.T))
        except numpy.linalg.linalg.LinAlgError:
            pass
    # TODO: this matrix has been already calculated before
    M = numpy.linalg.inv((A.T.dot(A))).dot(A.T)
    if cove is None:
        return (M * vare.reshape((1, m))).dot(M.T)
    else:
        return M.dot(cove).dot(M.T)


def lstsq_std(A, b=None, x=None, vare=None, cove=None):
    """Estimated error of solution to linear system

    .. math::

        A.x = b + e

        E(e) = 0

    Args:
        A(array): (m x n)
        b(array): only needed when neither vare nor cove are given (m)
        x(array): only needed when neither vare nor cove are given (n)
        vare(array): variance on e (m)
        cove(array): covariance matrix of e (m x m)

    Returns:
        stdx(array): errors (n)
    """
    if vare is None and cove is None:
        vare = numpy.var(numpy.dot(A, x) - b, ddof=x.size)
        vare = numpy.array([vare] * b.size)
    return numpy.sqrt(numpy.diag(lstsq_cov(A, vare=vare, cove=cove)))


def lstsq_std_indep(A, b=None, x=None, vare=None):
    """Estimated error of solution to linear system

    .. math::

        A.x = b + e

        E(e) = 0

    Assume we know x are independent random variables then
    there variances are found by solving another linear system

    .. math::
        (A*A).VAR(x) = VAR(e)

    Args:
        A(array): (m x n)
        b(array): (m)
        x(array): (n)
        vare(array): variance on e (m)

    Returns:
        stdx(array): sqrt(VARX) (n)
    """
    if vare is None:
        vare = numpy.var(numpy.dot(A, x) - b, ddof=x.size)
        vare = numpy.full(vare, x.size)
    return numpy.sqrt(lstsq(A * A, vare))


def lstsq(A, b, errors=False, vare=None, cove=None):
    """Solve the following linear system

    .. math::

        A.x = b + e

        E(e) = 0

    Args:
        A(array): (m x n)
        b(array): (m)
        errors(Optional(bool)): return solution with estimated error
        vare(array): variance on e (m)
        cove(array): covariance matrix of e (m x m)

    Returns:
        x(array): solution (n)
        stdx(array): optional errors (n)
    """
    x = numpy.linalg.lstsq(A, b, rcond=-1)[0]
    if errors:
        return x, lstsq_std(A, b=b, x=x, vare=vare, cove=cove)
    else:
        return x


def lstsq_nonnegative(A, b, errors=False, vare=None):
    """Solve the following linear system

    .. math::

        A.x = b + e \\quad x>=0

        E(e) = 0

    Args:
        A(array): (m x n)
        b(array): (m)
        errors(Optional(bool)): return solution with estimated error
        vare(array): variance on e (m)

    Returns:
        x(array): solution (n)
        stdx(array): optional errors (n)
    """
    if nnls is None:
        raise RuntimeError("requires 'scipy'")
    x = nnls(A, b)[0]
    if errors:
        return x, lstsq_std(A, b=b, x=x, vare=vare)
    else:
        return x


def lstsq_bound(A, b, lb, ub, errors=False, vare=None):
    r"""Solve the following linear system

    .. math::

        A.x = b + e \quad lb<=x<=ub

        E(e) = 0

    Args:
        A(array): (m x n)
        b(array): (m)
        lb(num): lower bound
        ub(num): upper bound
        errors(Optional(bool)): return solution with estimated error
        vare(array): variance on e (m)

    Returns:
        x(array): solution (n)
        stdx(array): optional errors (n)
    """
    if lsq_linear is None:
        raise RuntimeError("requires 'lsq_linear'")
    x = lsq_linear(A, b, bounds=(lb, ub)).x
    if errors:
        return x, lstsq_std(A, b=b, x=x, vare=vare)
    else:
        return x


def linfit(x, y, errors=False, vare=None):
    """Linear fit

    .. math::

        y = m.x + b + e

        E(e) = 0

    Args:
        x(array): (m)
        y(array): (m)
        errors(Optional(bool)): return solution with estimated error
        vare(array): variance on e (m)

    Returns:
        sol(array): solution (m,b)
        stdsol(array): optional errors (2-tuple)
    """
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    return lstsq(A, y, errors=errors, vare=vare)  # slope,intercept


def linfit2(x, y, errors=False, vare=None):
    if vare is not None:
        raise NotImplementedError("Use linfit instead")
    n = len(x)
    Sxy = (x * y).sum()
    Sxx = (x * x).sum()
    Sx = x.sum()
    Sy = y.sum()
    denom = float(n * Sxx - Sx * Sx)
    mnum = n * Sxy - Sx * Sy
    bnum = Sxx * Sy - Sx * Sxy
    m = mnum / denom
    b = bnum / denom

    if errors:
        Syy = (y * y).sum()
        num = n * Syy - Sy * Sy - m * mnum
        mstd = numpy.sqrt(num / ((n - 2.0) * denom))
        bstd = numpy.sqrt(num * Sxx / (n * (n - 2.0) * denom))
        return [m, b], [mstd, bstd]
    else:
        return [m, b]


def nanlinfit(x, y, errors=False, vare=None):
    x, y = xyremovenan(x, y)
    return linfit(x, y, errors=errors, vare=vare)


def nanlinfit2(x, y, errors=False, vare=None):
    x, y = xyremovenan(x, y)
    return linfit2(x, y, errors=errors, vare=vare)


def linfit_zerointercept(x, y, errors=False, vare=None):
    """Linear fit with zero intercept

    .. math::

        y = m.x + e

        E(e) = 0

    Args:
        x(array): (m)
        y(array): (m)
        errors(Optional(bool)): return solution with estimated error
        vare(array): variance on e (m)

    Returns:
        m(array): solution
        stdm(array): optional error
    """
    A = numpy.vstack([x]).T
    if errors:
        m, mstd = lstsq(A, y, errors=True, vare=vare)
        return m[0], mstd[0]
    else:
        return lstsq(A, y)[0]


def linfit_zerointercept2(x, y, errors=False, vare=None):
    Sxy = (x * y).sum()
    Sxx = float((x * x).sum())
    m = Sxy / Sxx
    if errors:
        n = len(x)
        Syy = (y * y).sum()
        mstd = numpy.sqrt(
            (Syy + m * m * Sxx - 2 * m * Sxy) / ((n - 1.0) * Sxx)
        )  # Not sure
        return m, mstd
    return m
