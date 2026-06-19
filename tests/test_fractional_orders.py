import numpy as np

import functions as fn
from fractional import gl_point_from_zero


def test_power_fraction_matches_gamma():
    spec = fn.get("x2")
    val = gl_point_from_zero(spec.f, 2.0, 0.5, 0.005)
    ref = float(spec.exact_frac(np.array([2.0]), 0.5)[0])
    assert abs(val - ref) < 0.01


def test_first_order_convergence_power_frac():
    spec = fn.get("x2")
    ref = float(spec.exact_frac(np.array([2.0]), 0.5)[0])
    e1 = abs(gl_point_from_zero(spec.f, 2.0, 0.5, 0.02) - ref)
    e2 = abs(gl_point_from_zero(spec.f, 2.0, 0.5, 0.01) - ref)
    assert 1.7 < e1 / e2 < 2.3


def test_from_zero_uses_floor_grid_count():
    calls = []

    def f(x):
        calls.extend(np.asarray(x, dtype=float).tolist())
        return np.asarray(x, dtype=float)

    gl_point_from_zero(f, 1.05, 1.0, 0.1)

    assert len(calls) == 11
    assert np.isclose(calls[-1], 0.05)
