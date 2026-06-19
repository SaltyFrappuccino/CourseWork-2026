import numpy as np
from scipy.special import gamma


def gl_coefficients(alpha, n):
    c = np.empty(n + 1)
    c[0] = 1.0
    if n >= 1:
        k = np.arange(1, n + 1)
        c[1:] = np.cumprod((k - 1 - alpha) / k)
    return c


def gl_point(f, x, alpha, h, n, coeffs=None):
    if coeffs is None:
        coeffs = gl_coefficients(alpha, n)
    k = np.arange(n + 1)
    vals = np.asarray(f(x - k * h), dtype=float)
    return float(coeffs @ vals / h ** alpha)


def gl_grid(f, xs, alpha, h, n):
    coeffs = gl_coefficients(alpha, n)
    xs = np.asarray(xs, dtype=float)
    k = np.arange(n + 1)
    nodes = xs[:, None] - k[None, :] * h
    vals = np.asarray(f(nodes), dtype=float)
    return vals @ coeffs / h ** alpha


def gl_grid_right(f, xs, alpha, h, n):
    coeffs = gl_coefficients(alpha, n)
    xs = np.asarray(xs, dtype=float)
    k = np.arange(n + 1)
    nodes = xs[:, None] + k[None, :] * h
    vals = np.asarray(f(nodes), dtype=float)
    return vals @ coeffs / h ** alpha


def gl_point_from_zero(f, x, alpha, h, coeffs=None):
    n = int(np.floor(x / h + 1e-12))
    k = np.arange(n + 1)
    if coeffs is None:
        coeffs = gl_coefficients(alpha, n)
    vals = np.asarray(f(x - k * h), dtype=float)
    return float(coeffs[:n + 1] @ vals / h ** alpha)


def gl_grid_from_zero(f, xs, alpha, h):
    xs = np.asarray(xs, dtype=float)
    if xs.size == 0:
        return np.empty(0)
    nmax = int(np.floor(xs.max() / h + 1e-12))
    coeffs = gl_coefficients(alpha, nmax)
    return np.array([gl_point_from_zero(f, float(x), alpha, h, coeffs) for x in xs])


def richardson_point(f, x, alpha, h, n):
    coarse = gl_point(f, x, alpha, h, n)
    fine = gl_point(f, x, alpha, h / 2.0, 2 * n)
    return 2.0 * fine - coarse


def richardson_from_zero(f, x, alpha, h):
    coarse = gl_point_from_zero(f, x, alpha, h)
    fine = gl_point_from_zero(f, x, alpha, h / 2.0)
    return 2.0 * fine - coarse


def coefficient_partial_sums(alpha, n):
    return np.cumsum(gl_coefficients(alpha, n))


def gl_shifted_grid(f, xs, alpha, h, n, p=1.0):
    coeffs = gl_coefficients(alpha, n)
    xs = np.asarray(xs, dtype=float)
    k = np.arange(n + 1)
    nodes = xs[:, None] - (k[None, :] - p) * h
    vals = np.asarray(f(nodes), dtype=float)
    return vals @ coeffs / h ** alpha


def gl_shifted_point_from_zero(f, x, alpha, h, p=1.0):
    n = int(np.floor(x / h + p + 1e-12))
    coeffs = gl_coefficients(alpha, n)
    k = np.arange(n + 1)
    nodes = x - (k - p) * h
    vals = np.asarray(f(nodes), dtype=float)
    return float(coeffs @ vals / h ** alpha)


def caputo_l1_point(f, x, alpha, h):
    n = int(np.floor(x / h + 1e-12))
    t = np.arange(n + 1) * h
    fv = np.asarray(f(t), dtype=float)
    j = np.arange(1, n + 1)
    b = j ** (1.0 - alpha) - (j - 1) ** (1.0 - alpha)
    diffs = fv[1:] - fv[:-1]
    return float(np.dot(b, diffs[::-1]) / (gamma(2.0 - alpha) * h ** alpha))


def caputo_l1_grid(f, xs, alpha, h):
    return np.array([caputo_l1_point(f, x, alpha, h) for x in np.asarray(xs, dtype=float)])
