import numpy as np
from scipy.special import gamma

import experiments as ex


def test_master_table_power_cell_matches_gamma():
    mt = ex.master_table(0.01, 500)
    row = mt[mt["функция"] == "x^2"].iloc[0]
    exact_half = gamma(3.0) / gamma(2.5) * 2.0 ** 1.5
    assert abs(row["D^0.5"] - exact_half) < 0.02
    assert abs(row["D^2"] - 2.0) < 1e-6


def test_master_table_constant_is_memory_term():
    mt = ex.master_table(0.01, 500)
    row = mt[mt["функция"] == "1"].iloc[0]
    exact = 2.0 ** (-0.5) / gamma(0.5)
    assert abs(row["D^0.5"] - exact) < 0.02
