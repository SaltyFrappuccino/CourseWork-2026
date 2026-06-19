import numpy as np

import functions as fn


def test_ln_out_of_domain_is_nan():
    spec = fn.get("ln")
    out = spec.f(np.array([-1.0, 0.0, 1.0]))
    assert np.isnan(out[0]) and np.isnan(out[1])
    assert not np.isnan(out[2])
