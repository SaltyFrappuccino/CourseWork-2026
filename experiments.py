import numpy as np
import pandas as pd
from scipy.special import gamma

import functions as fn
from fractional import (gl_grid, gl_point, gl_point_from_zero, gl_grid_from_zero,
                       gl_coefficients, richardson_point, richardson_from_zero,
                       coefficient_partial_sums, gl_shifted_point_from_zero,
                       caputo_l1_point)


def _successive_ratios(errors):
    ratios = [np.nan]
    for prev, cur in zip(errors, errors[1:]):
        ratios.append(prev / cur if prev > 0 and cur > 0 else np.nan)
    return ratios


def _method_errors(hs, exact, methods):
    table = {"h": list(hs)}
    for err_col, ratio_col, estimate in methods:
        errors = [abs(estimate(h) - exact) for h in hs]
        table[err_col] = errors
        table[ratio_col] = _successive_ratios(errors)
    return pd.DataFrame(table)


def table_values(func_key, xs, alphas, h, N):
    spec = fn.get(func_key)
    data = {"x": xs, "f(x)": spec.f(xs)}
    for a in alphas:
        data[f"D^{a:g}"] = gl_grid(spec.f, xs, a, h, N)
    return pd.DataFrame(data)


def table_values_from_zero(func_key, xs, alphas, h):
    spec = fn.get(func_key)
    data = {"x": xs, "f(x)": spec.f(xs)}
    for a in alphas:
        data[f"D^{a:g}"] = gl_grid_from_zero(spec.f, xs, a, h)
    return pd.DataFrame(data)


def master_table(h=0.01, N=500):
    alphas = [0.0, 0.5, 1.0, 1.5, 2.0]
    rows = []

    def add(label, x0, regime, values):
        row = {"функция": label, "x0": x0, "режим": regime}
        for a, v in zip(alphas, values):
            row[f"D^{a:g}"] = v
        rows.append(row)

    for key in ["one", "x", "x2", "x3"]:
        spec = fn.get(key)
        add(spec.label, 2.0, "a=0",
            [gl_point_from_zero(spec.f, 2.0, a, h) for a in alphas])

    for key in ["exp", "sin", "cos", "sin_plus_cos", "ln", "xsin", "xexp"]:
        spec = fn.get(key)
        x0 = 8.0 if key == "ln" else 1.0
        add(spec.label, x0, f"память L={N * h:g}",
            [gl_point(spec.f, x0, a, h, N) for a in alphas])

    spec = fn.get("tan")
    add(spec.label, 1.0, "память L=1",
        [gl_point(spec.f, 1.0, a, h, 100) for a in alphas])

    return pd.DataFrame(rows)


def regime_comparison(func_key, alpha, x, h, L, N_fixed):
    spec = fn.get(func_key)
    exact = float(spec.exact_frac(np.array([x]), alpha)[0])
    rows = [
        {"режим": "a=0 (N=x/h)", "N": int(round(x / h)),
         "значение": gl_point_from_zero(spec.f, x, alpha, h)},
        {"режим": f"память L={L:g}", "N": int(round(L / h)),
         "значение": gl_point(spec.f, x, alpha, h, int(round(L / h)))},
        {"режим": f"N={N_fixed}", "N": N_fixed,
         "значение": gl_point(spec.f, x, alpha, h, N_fixed)},
    ]
    df = pd.DataFrame(rows)
    df["эталон a=0"] = exact
    return df


def compare_classical(func_keys, xs, h, N, order):
    rows = []
    for key in func_keys:
        spec = fn.get(key)
        if order not in spec.classical:
            continue
        gl = gl_grid(spec.f, xs, float(order), h, N)
        exact = spec.classical[order](xs)
        for x, g, e in zip(xs, gl, exact):
            rows.append({
                "функция": spec.label,
                "x": x,
                "ГЛ": g,
                "точная": e,
                "абс. ошибка": abs(g - e),
                "отн. ошибка": abs(g - e) / max(1.0, abs(e)),
            })
    return pd.DataFrame(rows)


def h_influence(func_key, order, hs, xs, N):
    spec = fn.get(func_key)
    exact = spec.classical[order](xs)
    rows = []
    for h in hs:
        gl = gl_grid(spec.f, xs, float(order), h, N)
        err = np.abs(gl - exact)
        rows.append({"h": h, "N": N, "L=N*h": N * h,
                     "макс. ошибка": np.nanmax(err),
                     "сред. ошибка": np.nanmean(err)})
    return pd.DataFrame(rows)


def N_influence(func_key, alpha, Ns, h, xs):
    spec = fn.get(func_key)
    ref = spec.exact_frac(xs, alpha)
    rows = []
    for N in Ns:
        gl = gl_grid(spec.f, xs, alpha, h, N)
        err = np.abs(gl - ref)
        rows.append({"N": N, "L=N*h": N * h,
                     "макс. ошибка": np.nanmax(err),
                     "сред. ошибка": np.nanmean(err)})
    return pd.DataFrame(rows)


def convergence_integer(func_key, order, hs, x, N):
    spec = fn.get(func_key)
    exact = float(spec.classical[order](np.array([x]))[0])
    gls = [gl_point(spec.f, x, float(order), h, N) for h in hs]
    errs = [abs(gl - exact) for gl in gls]
    return pd.DataFrame({
        "h": list(hs),
        "ГЛ": gls,
        "точная": exact,
        "ошибка": errs,
        "ошибка(h)/ошибка(h/2)": _successive_ratios(errs),
    })


def convergence_power_frac(func_key, alpha, hs, x):
    spec = fn.get(func_key)
    exact = float(spec.exact_frac(np.array([x]), alpha)[0])
    gls = [gl_point_from_zero(spec.f, x, alpha, h) for h in hs]
    errs = [abs(gl - exact) for gl in gls]
    return pd.DataFrame({
        "h": list(hs),
        "N=x/h": [int(round(x / h)) for h in hs],
        "ГЛ": gls,
        "точная": exact,
        "ошибка": errs,
        "ошибка(h)/ошибка(h/2)": _successive_ratios(errs),
    })


def coefficient_table(alphas, kmax):
    data = {"k": np.arange(kmax + 1)}
    for a in alphas:
        data[f"alpha={a:g}"] = gl_coefficients(a, kmax)
    return pd.DataFrame(data)


def coefficient_decay(alphas, kmax):
    return {a: np.abs(gl_coefficients(a, kmax)) for a in alphas}


def rounding_floor(func_key, order, hs, x, N):
    spec = fn.get(func_key)
    exact = float(spec.classical[order](np.array([x]))[0])
    rows = []
    for h in hs:
        gl = gl_point(spec.f, x, float(order), h, N)
        rows.append({"h": h, "ГЛ": gl, "ошибка": abs(gl - exact)})
    return pd.DataFrame(rows)


def richardson_convergence(func_key, order, hs, x, N):
    spec = fn.get(func_key)
    exact = float(spec.classical[order](np.array([x]))[0])
    return _method_errors(hs, exact, [
        ("ошибка (обычная)", "отнош. обычной",
         lambda h: gl_point(spec.f, x, float(order), h, N)),
        ("ошибка (Ричардсон)", "отнош. Ричардсона",
         lambda h: richardson_point(spec.f, x, float(order), h, N)),
    ])


def richardson_convergence_frac(func_key, alpha, hs, x):
    spec = fn.get(func_key)
    exact = float(spec.exact_frac(np.array([x]), alpha)[0])
    return _method_errors(hs, exact, [
        ("ошибка (обычная)", "отнош. обычной",
         lambda h: gl_point_from_zero(spec.f, x, alpha, h)),
        ("ошибка (Ричардсон)", "отнош. Ричардсона",
         lambda h: richardson_from_zero(spec.f, x, alpha, h)),
    ])


def truncation_order_N(func_key, alpha, Ns, h, xs):
    spec = fn.get(func_key)
    ref = spec.exact_frac(xs, alpha)
    rows = []
    prev_err = prev_N = None
    for N in Ns:
        gl = gl_grid(spec.f, xs, alpha, h, N)
        err = float(np.nanmax(np.abs(gl - ref)))
        slope = np.nan
        if prev_err is not None and err > 0 and prev_err > 0:
            slope = np.log(prev_err / err) / np.log(N / prev_N)
        rows.append({"N": N, "L=N*h": N * h, "макс. ошибка": err,
                     "оценка наклона": slope})
        prev_err, prev_N = err, N
    return pd.DataFrame(rows)


def coefficient_sum_table(alphas, ns, N):
    data = {"n": ns}
    for a in alphas:
        S = coefficient_partial_sums(a, N)
        data[f"alpha={a:g}"] = [S[n] for n in ns]
    return pd.DataFrame(data)


def atlas_matrix(func_key, alphas, xs, h, N):
    spec = fn.get(func_key)
    M = np.empty((len(alphas), len(xs)))
    for i, a in enumerate(alphas):
        M[i, :] = gl_grid(spec.f, xs, a, h, N)
    return M


def error_grid_hN(func_key, order, hs, Ns, xs):
    spec = fn.get(func_key)
    exact = spec.classical[order](xs)
    M = np.empty((len(hs), len(Ns)))
    for i, h in enumerate(hs):
        for j, N in enumerate(Ns):
            gl = gl_grid(spec.f, xs, float(order), h, N)
            M[i, j] = float(np.nanmax(np.abs(gl - exact)))
    return M


def error_grid_hN_frac(func_key, alpha, hs, Ns, xs):
    spec = fn.get(func_key)
    ref = spec.exact_frac(xs, alpha)
    M = np.empty((len(hs), len(Ns)))
    for i, h in enumerate(hs):
        for j, N in enumerate(Ns):
            gl = gl_grid(spec.f, xs, alpha, h, N)
            M[i, j] = float(np.nanmax(np.abs(gl - ref)))
    return M


def shifted_vs_standard(func_key, alpha, hs, x):
    spec = fn.get(func_key)
    exact = float(spec.exact_frac(np.array([x]), alpha)[0])
    return _method_errors(hs, exact, [
        ("ошибка ГЛ (p=0)", "отнош. ГЛ",
         lambda h: gl_point_from_zero(spec.f, x, alpha, h)),
        ("ошибка сдвиг (p=1)", "отнош. сдвиг",
         lambda h: gl_shifted_point_from_zero(spec.f, x, alpha, h)),
    ])


def gl_vs_caputo(func_key, alpha, xs, h):
    spec = fn.get(func_key)
    f0 = float(spec.f(np.array([0.0]))[0])
    glv = gl_grid_from_zero(spec.f, xs, alpha, h)
    rows = []
    for x, g in zip(xs, glv):
        cap = caputo_l1_point(spec.f, x, alpha, h)
        corr = f0 * x ** (-alpha) / gamma(1.0 - alpha)
        rows.append({"x": x, "ГЛ (a=0)": g, "Капуто (L1)": cap,
                     "ГЛ - Капуто": g - cap,
                     "f(0)*x^{-a}/Г(1-a)": corr})
    return pd.DataFrame(rows)
