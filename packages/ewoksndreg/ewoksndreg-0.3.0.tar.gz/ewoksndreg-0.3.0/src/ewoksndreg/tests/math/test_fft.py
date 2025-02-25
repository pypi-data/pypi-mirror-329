import numpy
import pytest
from ...math import fft


# http://dsp.stackexchange.com/questions/633/what-data-should-i-use-to-test-an-fft-implementation-and-what-accuracy-should-i
# http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.38.3924


@pytest.mark.parametrize("convention", [fft.fftConvention.numpy, fft.fftConvention.idl])
@pytest.mark.parametrize("dx", [1, 0.5])
@pytest.mark.parametrize("dy", [1, 0.5])
@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_dirac_delta(convention, dx, dy, nx):
    sig = numpy.zeros(nx)
    sig[0] = 1
    ftsig1 = fft.fft(sig, dx=dx, normconvention=convention)
    ftsig2 = numpy.ones(nx, dtype=complex)
    if convention == fft.fftConvention.idl:
        ftsig2 /= nx
    numpy.testing.assert_allclose(ftsig1, ftsig2)

    ftsig = numpy.ones(nx)
    sig1 = fft.ifft1(ftsig, dx=dx, normconvention=convention)
    sig2 = numpy.zeros(nx, dtype=complex)
    sig2[0] = 1
    if convention == fft.fftConvention.idl:
        sig2[0] = nx
    numpy.testing.assert_allclose(sig1, sig2, atol=1e-10)

    for ny in range(4, 6):
        sig = numpy.zeros((ny, nx))
        sig[0, 0] = 1
        ftsig1 = fft.fft(sig, dx=dx, dy=dy, normconvention=convention)
        ftsig2 = numpy.ones((ny, nx), dtype=complex)
        if convention == fft.fftConvention.idl:
            ftsig2 /= nx * ny
        numpy.testing.assert_allclose(ftsig1, ftsig2)

        ftsig = numpy.ones((ny, nx))
        sig1 = fft.ifft(ftsig, dx=dx, dy=dy, normconvention=convention)
        sig2 = numpy.zeros((ny, nx), dtype=complex)
        sig2[0, 0] = 1
        if convention == fft.fftConvention.idl:
            sig2[0, 0] = nx * ny
        numpy.testing.assert_allclose(sig1, sig2, atol=1e-10)


@pytest.mark.parametrize("convention", [fft.fftConvention.numpy, fft.fftConvention.idl])
@pytest.mark.parametrize("dx", [1, 0.5])
@pytest.mark.parametrize("dy", [1, 0.5])
@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_consistent(convention, dx, dy, nx):
    sig = numpy.random.rand(nx)
    numpy.testing.assert_allclose(
        sig,
        fft.ifft1(
            fft.fft(sig, dx=dx, normconvention=convention),
            dx=dx,
            normconvention=convention,
        ),
    )
    numpy.testing.assert_allclose(
        sig,
        fft.fft(
            fft.ifft1(sig, dx=dx, normconvention=convention),
            dx=dx,
            normconvention=convention,
        ),
    )
    numpy.testing.assert_allclose(
        fft.fft(sig, dx=dx), fft.fft(sig, dx=dx, u=fft.fftfreq(nx, dx))
    )
    for ny in range(4, 6):
        sig = numpy.random.rand(ny, nx)
        numpy.testing.assert_allclose(
            sig,
            fft.ifft(
                fft.fft(sig, dx=dx, dy=dy, normconvention=convention),
                dx=dx,
                dy=dy,
                normconvention=convention,
            ),
        )
        numpy.testing.assert_allclose(
            sig,
            fft.fft(
                fft.ifft(sig, dx=dx, dy=dy, normconvention=convention),
                dx=dx,
                dy=dy,
                normconvention=convention,
            ),
        )
        numpy.testing.assert_allclose(
            fft.fft(sig, dx=dx, dy=dy),
            fft.fft(
                sig,
                dx=dx,
                dy=dy,
                u=fft.fftfreq(nx, dx),
                v=fft.fftfreq(ny, dy),
            ),
        )


@pytest.mark.parametrize("dx", [1, 0.5])
@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_linear(dx, nx):
    x = numpy.random.rand(nx)
    y = numpy.random.rand(nx)
    a = numpy.random.rand(1)[0]
    b = numpy.random.rand(1)[0]
    numpy.testing.assert_allclose(
        fft.fft(a * x + b * y, dx=dx),
        a * fft.fft(x, dx=dx) + b * fft.fft(y, dx=dx),
    )
    numpy.testing.assert_allclose(
        fft.ifft1(a * x + b * y, dx=dx),
        a * fft.ifft1(x, dx=dx) + b * fft.ifft1(y, dx=dx),
    )
    for ny in range(4, 6):
        x = numpy.random.rand(ny, nx)
        y = numpy.random.rand(ny, nx)
        a = numpy.random.rand(1)[0]
        b = numpy.random.rand(1)[0]
        numpy.testing.assert_allclose(
            fft.fft(a * x + b * y, dx=dx),
            a * fft.fft(x, dx=dx) + b * fft.fft(y, dx=dx),
        )
        numpy.testing.assert_allclose(
            fft.ifft(a * x + b * y, dx=dx),
            a * fft.ifft(x, dx=dx) + b * fft.ifft(y, dx=dx),
        )


@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_comp_np(nx):
    sig = numpy.random.rand(nx)
    numpy.testing.assert_allclose(
        numpy.fft.fft(sig), fft.fft(sig, normconvention=fft.fftConvention.numpy)
    )
    numpy.testing.assert_allclose(
        numpy.fft.ifft(sig), fft.ifft1(sig, normconvention=fft.fftConvention.numpy)
    )
    for ny in range(4, 6):
        sig = numpy.random.rand(ny, nx)
        numpy.testing.assert_allclose(
            numpy.fft.fft2(sig),
            fft.fft(sig, normconvention=fft.fftConvention.numpy),
        )
        numpy.testing.assert_allclose(
            numpy.fft.ifft2(sig),
            fft.ifft(sig, normconvention=fft.fftConvention.numpy),
        )

    # Force using non-numpy code
    sig = numpy.random.rand(nx)
    u = fft.fftfreq(nx)
    numpy.testing.assert_allclose(
        numpy.fft.fft(sig), fft.fft(sig, normconvention=fft.fftConvention.numpy, u=u)
    )
    numpy.testing.assert_allclose(
        numpy.fft.ifft(sig),
        fft.ifft(sig, normconvention=fft.fftConvention.numpy, u=u),
    )
    for ny in range(4, 6):
        v = fft.fftfreq(ny)
        sig = numpy.random.rand(ny, nx)
        numpy.testing.assert_allclose(
            numpy.fft.fft2(sig),
            fft.fft(sig, normconvention=fft.fftConvention.numpy, u=u, v=v),
        )
        numpy.testing.assert_allclose(
            numpy.fft.ifft2(sig),
            fft.ifft(sig, normconvention=fft.fftConvention.numpy, u=u, v=v),
        )


@pytest.mark.parametrize("dx", [1, 0.5])
@pytest.mark.parametrize("dy", [1, 0.5])
@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_shift(dx, dy, nx):
    sig1 = numpy.zeros(nx)
    sig1[0] = 1
    sig2 = numpy.zeros(nx)
    ox = 1 + numpy.random.rand(1)[0] * (nx - 2)
    ox = int(ox)
    sig2[ox] = 1
    ftsig1 = fft.fft(sig1, dx=dx)
    ftsig2 = fft.fft(sig2, dx=dx) * numpy.exp(
        2j * numpy.pi * fft.fftfreq(nx, d=dx) * ox * dx
    )
    numpy.testing.assert_allclose(ftsig1, ftsig2)

    for ny in range(4, 6):
        sig1 = numpy.zeros((ny, nx))
        sig1[0, 0] = 1
        sig2 = numpy.zeros((ny, nx))
        ox, oy = 1 + numpy.random.rand(2) * (numpy.array([nx, ny]) - 2)
        ox = int(ox)
        oy = int(oy)
        sig2[oy, ox] = 1
        ftsig1 = fft.fft(sig1, dx=dx, dy=dy)
        ftsig2 = fft.fft(sig2, dx=dx, dy=dy) * numpy.exp(
            2j
            * numpy.pi
            * (
                numpy.add.outer(
                    fft.fftfreq(ny, d=dy) * oy * dy,
                    fft.fftfreq(nx, d=dx) * ox * dx,
                )
            )
        )
        numpy.testing.assert_allclose(ftsig1, ftsig2)


@pytest.mark.parametrize(
    "freqconvention", [fft.fftConvention.numpy, fft.fftConvention.idl]
)
@pytest.mark.parametrize("dx", [1, 0.5])
@pytest.mark.parametrize("dy", [1, 0.5])
@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_freq(freqconvention, dx, dy, nx):
    sig = numpy.random.rand(nx)
    ftsig = fft.fftshift(fft.fft(sig, dx=dx), freqconvention=freqconvention)
    freq = fft.fftshift(
        fft.fftfreq(nx, d=dx, freqconvention=freqconvention),
        freqconvention=freqconvention,
    )
    assert all(numpy.diff(freq) > 0)
    if nx % 2 == 1:
        assert ftsig[0] == numpy.conj(ftsig[-1])

    for ny in range(4, 6):
        sig = numpy.random.rand(ny, nx)
        ftsig = fft.fftshift(
            fft.fft(sig, dx=dx, dy=dy),
            freqconvention=freqconvention,
        )
        u = fft.fftshift(
            fft.fftfreq(nx, d=dx, freqconvention=freqconvention),
            freqconvention=freqconvention,
        )
        v = fft.fftshift(
            fft.fftfreq(ny, d=dy, freqconvention=freqconvention),
            freqconvention=freqconvention,
        )
        assert all(numpy.diff(u) > 0)
        assert all(numpy.diff(v) > 0)
        if nx % 2 == 1 and ny % 2 == 1:
            assert numpy.conj(ftsig[-1, -1]) == ftsig[0, 0]


@pytest.mark.parametrize(
    "freqconvention", [fft.fftConvention.numpy, fft.fftConvention.idl]
)
@pytest.mark.parametrize("dx", [1, 0.5])
@pytest.mark.parametrize("dy", [1, 0.5])
@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_subregion(freqconvention, dx, dy, nx):
    sig = numpy.random.rand(nx)
    ftsig = fft.fft(sig, dx=dx)
    # subregion in real space:
    numpy.testing.assert_allclose(
        sig[1 : nx - 1], fft.ifft1(ftsig, dx=dx, x0=1, x1=nx - 2)
    )
    # subregion in Fourier space:
    u = fft.fftshift(
        fft.fftfreq(nx, d=dx, freqconvention=freqconvention),
        freqconvention=freqconvention,
    )
    numpy.testing.assert_allclose(
        fft.fftshift(ftsig, freqconvention=freqconvention)[1 : nx - 1],
        fft.fft(sig, dx=dx, u=u[1 : nx - 1]),
    )
    for ny in range(4, 6):
        sig = numpy.random.rand(ny, nx)
        ftsig = fft.fft(sig, dx=dx, dy=dy)
        # subregion in real space:
        numpy.testing.assert_allclose(
            sig[1 : ny - 1, 1 : nx - 1],
            fft.ifft(
                ftsig,
                dx=dx,
                x0=1,
                x1=nx - 2,
                dy=dy,
                y0=1,
                y1=ny - 2,
            ),
        )
        # subregion in Fourier space:
        u = fft.fftshift(
            fft.fftfreq(nx, d=dx, freqconvention=freqconvention),
            freqconvention=freqconvention,
        )
        v = fft.fftshift(
            fft.fftfreq(ny, d=dy, freqconvention=freqconvention),
            freqconvention=freqconvention,
        )
        numpy.testing.assert_allclose(
            fft.fftshift(ftsig, freqconvention=freqconvention)[1 : ny - 1, 1 : nx - 1],
            fft.fft(sig, dx=dx, u=u[1 : nx - 1], dy=dy, v=v[1 : ny - 1]),
        )


@pytest.mark.parametrize("nx", list(range(4, 6)))
def test_center(nx):
    sig = numpy.random.rand(nx)
    numpy.testing.assert_allclose(
        fft.fftshift(fft.fft(sig)), fft.fft(sig, centered=True)
    )
    numpy.testing.assert_allclose(
        fft.fftshift(fft.fftfreq(nx)), fft.fftfreq(nx, centered=True)
    )
    numpy.testing.assert_allclose(
        sig, fft.ifft1(fft.fft(sig, centered=True), centered=True)
    )
    for ny in range(4, 6):
        sig = numpy.random.rand(ny, nx)
        numpy.testing.assert_allclose(
            fft.fftshift(fft.fft(sig)), fft.fft(sig, centered=True)
        )
        numpy.testing.assert_allclose(
            sig,
            fft.ifft(fft.fft(sig, centered=True), centered=True),
        )
