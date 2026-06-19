import numpy as np
from scipy.special import gamma

import functions as fn
from fractional import (gl_shifted_point_from_zero, gl_point_from_zero,
                        caputo_l1_point)


def test_shifted_matches_gamma():
    spec = fn.get("x2")
    ref = float(spec.exact_frac(np.array([2.0]), 0.5)[0])
    val = gl_shifted_point_from_zero(spec.f, 2.0, 0.5, 0.002)
    assert abs(val - ref) < 0.02


def test_shifted_is_first_order():
    spec = fn.get("x2")
    ref = float(spec.exact_frac(np.array([2.0]), 0.5)[0])
    e1 = abs(gl_shifted_point_from_zero(spec.f, 2.0, 0.5, 0.02) - ref)
    e2 = abs(gl_shifted_point_from_zero(spec.f, 2.0, 0.5, 0.01) - ref)
    assert 1.7 < e1 / e2 < 2.3


def test_caputo_of_constant_is_zero():
    spec = fn.get("one")
    assert abs(caputo_l1_point(spec.f, 2.0, 0.5, 0.01)) < 1e-9


def test_caputo_matches_gamma_for_power():
    spec = fn.get("x2")
    ref = float(spec.exact_frac(np.array([2.0]), 0.5)[0])
    val = caputo_l1_point(spec.f, 2.0, 0.5, 0.005)
    assert abs(val - ref) < 0.01


def test_gl_minus_caputo_is_lower_terminal_term():
    spec = fn.get("exp")
    x, alpha, h = 1.5, 0.5, 0.002
    gap = gl_point_from_zero(spec.f, x, alpha, h) - caputo_l1_point(spec.f, x, alpha, h)
    corr = 1.0 * x ** (-alpha) / gamma(1.0 - alpha)
    assert abs(gap - corr) < 0.02
