"""Calculate active transformation between two sets of coordinates"""

from typing import Sequence
import numpy

try:
    from scipy.stats import trim_mean
except ImportError:

    def trim_mean(arr, proportiontocut, axis=0):
        arr = numpy.asarray(arr)

        if arr.size == 0:
            return numpy.nan

        if axis is None:
            arr = arr.ravel()
            axis = 0

        nobs = arr.shape[axis]
        lowercut = int(proportiontocut * nobs)
        uppercut = nobs - lowercut
        if lowercut > uppercut:
            raise ValueError("Proportion too big.")

        atmp = numpy.partition(arr, (lowercut, uppercut - 1), axis)

        sl = [slice(None)] * atmp.ndim
        sl[axis] = slice(lowercut, uppercut)
        return numpy.mean(atmp[tuple(sl)], axis=axis)


def calc_identity(
    from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    """Coordinate array shape is (ndim, ncoord)"""
    return numpy.identity(3, dtype=from_coord[0].dtype)


def calc_translation(
    from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    """Coordinate array shape is (ndim, ncoord)"""
    from_coord = numpy.asarray(from_coord)
    to_coord = numpy.asarray(to_coord)
    T = centroid(to_coord - from_coord, axis=-1)
    active = numpy.identity(3, dtype=T.dtype)
    active[0:2, 2] = T
    return active


def calc_rigid(
    from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    r"""Coordinate array shape is (ndim, ncoord).

    Find the proper-rigid transformation between two sets of coordinates by solving
    this system of equations (https://igl.ethz.ch/projects/ARAP/svd_rot.pdf):

    .. math::

        \begin{align*}
            X_c &= (X-Cen(X)) \\
            Y_c &= (Y-Cen(Y)) \\
            C.X + T &= X' \\
            T &= Cen(X') - C.Cen(X)
        \end{align*}

        \begin{align*}
            C.X_c &= Y_c \\
            H &= X_c . Y_c^T \\
            H &= U . S . V^T \\
            C &= V.U^T \\
        \end{align*}

        \begin{align*}
            C.X + T &= X' \\
            T &= Cen(X') - C.Cen(X)
        \end{align*}

    where `C` is found with singular value decomposition. The resulting transformation matrix is

    .. math::

        \begin{equation*}
            \begin{bmatrix}
                C & T\\
                0 & 1\\
            \end{bmatrix}
        \end{equation*}
    """
    from_coord = numpy.asarray(from_coord)
    to_coord = numpy.asarray(to_coord)
    from_cen = centroid(from_coord, axis=-1)[:, None]
    to_cen = centroid(to_coord, axis=-1)[:, None]
    from_coord_centered = from_coord - from_cen
    to_coord_centered = to_coord - to_cen

    H = numpy.dot(from_coord_centered, to_coord_centered.T)
    # H = U.dot(numpy.diag(s)).dot(Vt)
    U, s, Vt = numpy.linalg.svd(H, full_matrices=False)
    C = Vt.T.dot(U.T)

    # if numpy.linalg.det(C) < 0:
    #    Vt[2, :] *= -1
    #    C = Vt.T.dot(U.T)

    active = numpy.identity(3, dtype=C.dtype)
    active[0:2, 0:2] = C

    # The formula should be:
    # active[0:2, 2] = (to_cen - C.dot(from_cen)).flatten()
    # But this seems to be more precise:
    active[0:2, 2] = centroid(to_coord - C.dot(from_coord), axis=-1)

    return active


def calc_similarity(
    from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    r"""Coordinate array shape is (ndim, ncoord).

    Find the similarity transformation between two sets of coordinates by solving
    this system of equations:

    .. math::

        \begin{align*}
            x' &= a.x - b.y + t_0\\
            y' &= b.x + a.y + t_1\\
            \mathrm{\mathrm{sol}} &= [a, b, t_0, t_1]
        \end{align*}

    .. math::

        \begin{equation*}
            \begin{bmatrix}
                x_1 & -y1 &  1 &  0 \\
                y1 &  x_1 &  0 &  1 \\
                x_2 & -y_2 &  1 &  0 \\
                y_2 &  x_2 &  0 &  1 \\
                \vdots
            \end{bmatrix}.\mathrm{sol}=
            \begin{bmatrix}
                x_1' \\
                y1' \\
                x_2' \\
                y_2' \\
                \vdots
            \end{bmatrix}
        \end{equation*}

    The resulting transformation matrix is

    .. math::

        \begin{equation*}
            \mathrm{sol}=\begin{bmatrix}
                a & -b & t_0\\
                b & a & t_1\\
                0 & 0 & 1
            \end{bmatrix}
        \end{equation*}
    """

    N = len(from_coord[0])

    A = numpy.zeros((2 * N, 4))
    A[::2, 0] = from_coord[0]
    A[1::2, 0] = from_coord[1]
    A[::2, 1] = -from_coord[1]
    A[1::2, 1] = from_coord[0]
    A[::2, 2] = 1
    A[1::2, 3] = 1

    b = numpy.zeros((2 * N, 1))
    b[::2, 0] = to_coord[0]
    b[1::2, 0] = to_coord[1]

    sol = lstsq(A, b)
    active = numpy.identity(3, dtype=sol.dtype)
    active[0:2, 0:2] = [[sol[0], -sol[1]], [sol[1], sol[0]]]
    active[0:2, 2] = sol[2:].flatten()
    return active


def calc_affine(
    from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    r"""Coordinate array shape is (ndim, ncoord).

    Find the affine transformation between two sets of coordinates by solving
    this system of equations:

    .. math::

        \begin{align*}
            x' &= a.x + b.y + t_0\\
            y' &= c.x + d.y + t_1\\
            \mathrm{sol} &= [a, b, t_0, c, d, t_1]
        \end{align*}

    .. math::

        \begin{equation*}
            \begin{bmatrix}
                x_1 & y1 & 1 & 0 & 0 & 0 \\
                0 & 0 & 0 & x_1 & y1 & 1 \\
                x_2 & y_2 & 1 & 0 & 0 & 0 \\
                0 & 0 & 0 & x_2 & y_2 & 1 \\
                \vdots
            \end{bmatrix}. \mathrm{sol} =
            \begin{bmatrix}
                x_1' \\
                y1' \\
                x_2' \\
                y_2' \\
                \vdots
            \end{bmatrix}
        \end{equation*}

    The resulting transformation matrix is

    .. math::

        \begin{equation*}
            \mathrm{sol}=\begin{bmatrix}
                a & b & t_0\\
                c & d & t_1\\
                0 & 0 & 1
            \end{bmatrix}
        \end{equation*}
    """

    N = len(from_coord[0])

    A = numpy.zeros((2 * N, 6))
    A[::2, 0] = from_coord[0]
    A[::2, 1] = from_coord[1]
    A[::2, 2] = 1
    A[1::2, 3] = from_coord[0]
    A[1::2, 4] = from_coord[1]
    A[1::2, 5] = 1

    b = numpy.zeros((2 * N, 1))
    b[::2, 0] = to_coord[0]
    b[1::2, 0] = to_coord[1]

    sol = lstsq(A, b)
    active = numpy.identity(3, dtype=sol.dtype)
    active[0:2, :] = sol.reshape((2, 3))
    return active


def calc_projective(
    from_coord: Sequence[numpy.ndarray], to_coord: Sequence[numpy.ndarray]
) -> numpy.ndarray:
    r"""Coordinate array shape is (ndim, ncoord).

    Find the projective transformation between two sets of coordinates by solving
    this system of equations:

    .. math::

        \begin{align*}
            x' &= \frac{a.x + b.y + t_0}{p_x.x+p_y.y+1}
            y' &= \frac{c.x + d.y + t_1}{p_x.x+p_y.y+1}
            x' &= a.x + b.y + t_0 - p_x.x.x' - p_y.y.x'
            y' &= c.x + d.y + t_1 - p_x.x.y' - p_y.y.y'
            \mathrm{sol} &= [a, b, t_0, c, d, t_1 , p_x, p_y]
        \end{align*}

    .. math::

        \begin{equation*}
            \begin{bmatrix}
                x_1 & y1 & 1 & 0 & 0 & 0 & -x_1.x_1' & -y1.x_1'
                0  & 0 & 0 & x_1 & y1 & 1 & -x_1.y1' & -y1.y1'
                x_2 & y_2 & 1 & 0 & 0 & 0 & -x_2.x_2' & -y_2.x_2'
                0 & 0 & 0 & x_2 & y_2 & 1 & -x_2.y_2' & -y_2.y_2'
                \vdots
            \end{bmatrix}. \mathrm{sol} =
            \begin{bmatrix}
                x_1' \\
                y1' \\
                x_2' \\
                y_2' \\
                \vdots
            \end{bmatrix}
        \end{equation*}


    The resulting transformation matrix is

    .. math::

        \begin{equation*}
            \mathrm{sol}=\begin{bmatrix}
                a & b & t_0\\
                c & d & t_1\\
                p_x & p_y & 1
            \end{bmatrix}
        \end{equation*}

    """

    N = len(from_coord[0])

    A = numpy.zeros((2 * N, 8))
    A[::2, 0] = from_coord[0]
    A[::2, 1] = from_coord[1]
    A[::2, 2] = 1
    A[1::2, 3] = from_coord[0]
    A[1::2, 4] = from_coord[1]
    A[1::2, 5] = 1
    A[::2, 6] = -from_coord[0] * to_coord[0]
    A[1::2, 6] = -from_coord[0] * to_coord[1]
    A[::2, 7] = -from_coord[1] * to_coord[0]
    A[1::2, 7] = -from_coord[1] * to_coord[1]

    b = numpy.zeros((2 * N, 1))
    b[::2, 0] = to_coord[0]
    b[1::2, 0] = to_coord[1]

    sol = lstsq(A, b)
    return numpy.append(sol, 1).reshape((3, 3))


def centroid(arr: Sequence[numpy.ndarray], axis: int = 0) -> numpy.ndarray:
    try:
        return trim_mean(arr, 0.1, axis=axis)
    except ValueError:
        return numpy.median(arr, axis=axis)


def lstsq(A: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
    return numpy.linalg.lstsq(A, b, rcond=-1)[0].flatten()
