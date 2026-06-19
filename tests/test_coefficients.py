import numpy as np

from fractional import coefficient_partial_sums, gl_coefficients


def test_coefficients_recurrence():
    c = gl_coefficients(0.5, 4)
    expected = np.array([1.0, -0.5, -0.125, -0.0625, -0.0390625])
    assert np.allclose(c, expected)


def test_integer_order_coefficients_truncate():
    c1 = gl_coefficients(1.0, 5)
    assert np.allclose(c1, [1.0, -1.0, 0.0, 0.0, 0.0, 0.0])
    c2 = gl_coefficients(2.0, 5)
    assert np.allclose(c2, [1.0, -2.0, 1.0, 0.0, 0.0, 0.0])


def test_partial_sums_go_to_zero():
    sums = coefficient_partial_sums(0.5, 20000)
    assert abs(sums[-1]) < 0.01
    assert abs(sums[-1]) < abs(sums[100])
