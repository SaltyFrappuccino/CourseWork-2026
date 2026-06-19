from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from scipy.special import gamma, rgamma


def _arr(x):
    return np.asarray(x, dtype=float)


@dataclass
class FuncSpec:
    key: str
    label: str
    f: Callable
    interval: tuple
    classical: dict = field(default_factory=dict)
    exact_frac: Callable = None


def power_ref(beta):
    def ref(x, alpha):
        x = _arr(x)
        return gamma(beta + 1.0) * rgamma(beta - alpha + 1.0) * np.power(x, beta - alpha)
    return ref


def safe_ln(x):
    x = _arr(x)
    out = np.full_like(x, np.nan)
    ok = x > 0
    out[ok] = np.log(x[ok])
    return out


def tan_fn(x):
    return np.tan(_arr(x))


REGISTRY = {}


def reg(spec):
    REGISTRY[spec.key] = spec


reg(FuncSpec("one", "1",
             lambda x: np.ones_like(_arr(x)),
             (1.0, 5.0),
             {1: lambda x: np.zeros_like(_arr(x)), 2: lambda x: np.zeros_like(_arr(x))}))

reg(FuncSpec("x", "x",
             lambda x: _arr(x),
             (1.0, 5.0),
             {1: lambda x: np.ones_like(_arr(x)), 2: lambda x: np.zeros_like(_arr(x))},
             power_ref(1.0)))

reg(FuncSpec("x2", "x^2",
             lambda x: _arr(x) ** 2,
             (1.0, 5.0),
             {1: lambda x: 2.0 * _arr(x), 2: lambda x: np.full_like(_arr(x), 2.0)},
             power_ref(2.0)))

reg(FuncSpec("x3", "x^3",
             lambda x: _arr(x) ** 3,
             (1.0, 5.0),
             {1: lambda x: 3.0 * _arr(x) ** 2, 2: lambda x: 6.0 * _arr(x)},
             power_ref(3.0)))

reg(FuncSpec("exp", "e^x",
             lambda x: np.exp(_arr(x)),
             (0.0, 3.0),
             {1: lambda x: np.exp(_arr(x)), 2: lambda x: np.exp(_arr(x))},
             lambda x, alpha: np.exp(_arr(x))))

reg(FuncSpec("sin", "sin x",
             lambda x: np.sin(_arr(x)),
             (0.0, 4.0 * np.pi),
             {1: lambda x: np.cos(_arr(x)), 2: lambda x: -np.sin(_arr(x))},
             lambda x, alpha: np.sin(_arr(x) + np.pi * alpha / 2.0)))

reg(FuncSpec("cos", "cos x",
             lambda x: np.cos(_arr(x)),
             (0.0, 4.0 * np.pi),
             {1: lambda x: -np.sin(_arr(x)), 2: lambda x: -np.cos(_arr(x))},
             lambda x, alpha: np.cos(_arr(x) + np.pi * alpha / 2.0)))

reg(FuncSpec("tan", "tan x",
             tan_fn,
             (0.0, 1.3),
             {1: lambda x: 1.0 / np.cos(_arr(x)) ** 2}))

reg(FuncSpec("ln", "ln x",
             safe_ln,
             (6.0, 10.0),
             {1: lambda x: 1.0 / _arr(x), 2: lambda x: -1.0 / _arr(x) ** 2}))

reg(FuncSpec("xsin", "x*sin x",
             lambda x: _arr(x) * np.sin(_arr(x)),
             (0.0, 4.0 * np.pi),
             {1: lambda x: np.sin(_arr(x)) + _arr(x) * np.cos(_arr(x)),
              2: lambda x: 2.0 * np.cos(_arr(x)) - _arr(x) * np.sin(_arr(x))}))

reg(FuncSpec("xexp", "x*e^x",
             lambda x: _arr(x) * np.exp(_arr(x)),
             (0.0, 3.0),
             {1: lambda x: np.exp(_arr(x)) * (1.0 + _arr(x)),
              2: lambda x: np.exp(_arr(x)) * (2.0 + _arr(x))}))

reg(FuncSpec("sin_plus_cos", "sin x + cos x",
             lambda x: np.sin(_arr(x)) + np.cos(_arr(x)),
             (0.0, 4.0 * np.pi),
             {1: lambda x: np.cos(_arr(x)) - np.sin(_arr(x)),
              2: lambda x: -np.sin(_arr(x)) - np.cos(_arr(x))},
             lambda x, alpha: (np.sin(_arr(x) + np.pi * alpha / 2.0)
                               + np.cos(_arr(x) + np.pi * alpha / 2.0))))


def get(key):
    if key not in REGISTRY:
        raise KeyError(f"нет функции '{key}'. Есть: {', '.join(REGISTRY)}")
    return REGISTRY[key]


def names():
    return list(REGISTRY)
