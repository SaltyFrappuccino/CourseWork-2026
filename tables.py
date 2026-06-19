import os

import numpy as np
import pandas as pd

import experiments as ex

TABLES = os.path.join(os.path.dirname(__file__), "tables")

H_BASE = 0.01
N_BASE = 500


def build_all():
    os.makedirs(TABLES, exist_ok=True)
    out = {}

    out["master_table"] = ex.master_table(H_BASE, N_BASE)

    xs = np.linspace(0, 2 * np.pi, 9)
    out["sin_values"] = ex.table_values(
        "sin", xs, [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
        H_BASE, N_BASE)

    xs2 = np.linspace(1, 5, 9)
    out["x2_values"] = ex.table_values_from_zero(
        "x2", xs2, [0.0, 0.5, 1.0, 1.5, 2.0], H_BASE)

    xs3 = np.linspace(0.5, 5, 6)
    out["compare_alpha1"] = ex.compare_classical(
        ["x2", "exp", "sin", "cos"], xs3, H_BASE, N_BASE, order=1)

    xs4 = np.linspace(0.5, 2 * np.pi, 200)
    out["h_influence"] = ex.h_influence(
        "sin", 1, [0.1, 0.05, 0.02, 0.01, 0.005, 0.001], xs4, N_BASE)

    xs5 = np.linspace(np.pi, 3 * np.pi, 200)
    out["N_influence"] = ex.N_influence(
        "sin", 0.5, [5, 20, 50, 100, 300, 500, 1000], H_BASE, xs5)

    out["convergence_int"] = ex.convergence_integer(
        "sin", 1, [0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625], x=1.0, N=50)

    out["convergence_frac"] = ex.convergence_power_frac(
        "x2", 0.5, [0.04, 0.02, 0.01, 0.005, 0.0025, 0.00125], x=2.0)

    out["coefficients"] = ex.coefficient_table([0.0, 0.5, 1.0, 1.5, 2.0], kmax=6)

    out["rounding_floor"] = ex.rounding_floor(
        "sin", 1, [0.1, 0.01, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9,
                   1e-10, 1e-11], x=1.0, N=2)

    out["richardson"] = ex.richardson_convergence(
        "sin", 1, [0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625], x=1.0, N=2)

    out["richardson_frac"] = ex.richardson_convergence_frac(
        "x2", 0.5, [0.04, 0.02, 0.01, 0.005, 0.0025, 0.00125], x=2.0)

    xs6 = np.linspace(np.pi, 3 * np.pi, 200)
    out["truncation_N"] = ex.truncation_order_N(
        "sin", 0.5, [5, 20, 50, 100, 300, 500, 1000, 2000], H_BASE, xs6)

    out["coeff_sums"] = ex.coefficient_sum_table(
        [0.25, 0.5, 0.75], ns=[1, 5, 10, 50, 100, 500], N=500)

    out["x3_values"] = ex.table_values_from_zero(
        "x3", np.linspace(1, 4, 7), [0.0, 0.5, 1.0, 1.5, 2.0], H_BASE)

    out["xsin_values"] = ex.table_values(
        "xsin", np.linspace(0, 2 * np.pi, 9), [0.0, 0.5, 1.0, 2.0], H_BASE, N_BASE)

    out["regime_compare"] = ex.regime_comparison(
        "x2", 0.5, x=2.0, h=0.01, L=5.0, N_fixed=50)

    out["shifted_vs_standard"] = ex.shifted_vs_standard(
        "x2", 0.5, [0.04, 0.02, 0.01, 0.005, 0.0025], x=2.0)

    out["gl_vs_caputo"] = ex.gl_vs_caputo(
        "exp", 0.5, np.linspace(0.5, 2.5, 6), h=0.005)

    for name, df in out.items():
        df.to_csv(os.path.join(TABLES, f"{name}.csv"), index=False,
                  encoding="utf-8-sig")
    with pd.ExcelWriter(os.path.join(TABLES, "tables.xlsx")) as writer:
        for name, df in out.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    return out


if __name__ == "__main__":
    for name, df in build_all().items():
        print(f"\n=== {name} ===")
        print(df.to_string(index=False))
