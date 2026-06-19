import numpy as np

import functions as fn
from fractional import gl_grid, gl_point


def test_alpha0_is_identity():
    spec = fn.get("sin")
    xs = np.linspace(0.5, 6.0, 25)
    got = gl_grid(spec.f, xs, 0.0, 0.01, 500)
    assert np.allclose(got, spec.f(xs))


def test_alpha1_sin_matches_cos():
    spec = fn.get("sin")
    val = gl_point(spec.f, 1.0, 1.0, 0.01, 2)
    assert abs(val - np.cos(1.0)) < 0.01


def test_alpha2_x2_is_exact():
    spec = fn.get("x2")
    val = gl_point(spec.f, 2.3, 2.0, 0.01, 500)
    exact = float(spec.classical[2](np.array([2.3]))[0])
    assert abs(val - exact) < 1e-9


def test_first_order_convergence_sin():
    spec = fn.get("sin")
    exact = np.cos(1.0)
    e1 = abs(gl_point(spec.f, 1.0, 1.0, 0.02, 50) - exact)
    e2 = abs(gl_point(spec.f, 1.0, 1.0, 0.01, 50) - exact)
    assert 1.7 < e1 / e2 < 2.3
