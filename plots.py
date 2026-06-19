import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scipy.special import gamma

import functions as fn
from fractional import (gl_grid, gl_grid_right, gl_point, gl_point_from_zero,
                       gl_grid_from_zero, gl_coefficients,
                       coefficient_partial_sums, gl_shifted_point_from_zero,
                       caputo_l1_grid)
import experiments as ex

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "dejavusans",
    "figure.dpi": 130,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "savefig.bbox": "tight",
})

GRAPHS = os.path.join(os.path.dirname(__file__), "graphs")


def _save(fig, name):
    os.makedirs(GRAPHS, exist_ok=True)
    path = os.path.join(GRAPHS, name)
    fig.savefig(path)
    plt.close(fig)
    return path


def sin_orders(h=0.01, N=500):
    spec = fn.get("sin")
    xs = np.linspace(0, 4 * np.pi, 700)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for a in [0.0, 0.5, 1.0, 1.5, 2.0]:
        ax.plot(xs, gl_grid(spec.f, xs, a, h, N), label=fr"$\alpha = {a:g}$")
    ax.plot(xs, np.cos(xs), "k--", lw=1, alpha=0.6, label=r"$\cos x$ ($\alpha=1$)")
    ax.plot(xs, -np.sin(xs), "k:", lw=1, alpha=0.6, label=r"$-\sin x$ ($\alpha=2$)")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Дробные производные $\sin x$ при разных порядках $\alpha$")
    ax.legend(fontsize=8, ncol=2)
    return _save(fig, "sin_orders.png")


def alpha1_check(h=0.01, N=500):
    spec = fn.get("sin")
    xs = np.linspace(0, 2 * np.pi, 400)
    gl = gl_grid(spec.f, xs, 1.0, h, N)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(xs, gl, label=r"$D^1$ (ГЛ)", lw=2)
    ax.plot(xs, np.cos(xs), "r--", label=r"$\cos x$")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"$D^1 \sin x$ против $\cos x$")
    ax.legend(fontsize=9)
    return _save(fig, "alpha1_check.png")


def h_influence(N=500):
    spec = fn.get("sin")
    xs = np.linspace(0, 2 * np.pi, 500)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, np.cos(xs), "k-", lw=2, label=r"$\cos x$")
    for h, style in [(0.5, "C0--"), (0.2, "C1-."), (0.02, "C2:")]:
        ax.plot(xs, gl_grid(spec.f, xs, 1.0, h, N), style,
                label=fr"$h={h:g}$")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Влияние шага $h$ на $D^1 \sin x$")
    ax.legend(fontsize=9)
    return _save(fig, "h_influence.png")


def N_influence(h=0.01):
    spec = fn.get("sin")
    xs = np.linspace(np.pi, 3 * np.pi, 400)
    ref = spec.exact_frac(xs, 0.5)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, ref, "k-", lw=2, label=r"$\sin(x+\pi/4)$")
    for N, style in [(5, "C0--"), (20, "C1-."), (200, "C2:")]:
        ax.plot(xs, gl_grid(spec.f, xs, 0.5, h, N), style, label=fr"$N={N}$")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Влияние числа членов $N$ на $D^{0.5} \sin x$")
    ax.legend(fontsize=9)
    return _save(fig, "N_influence.png")


def coeff_decay(kmax=500):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    k = np.arange(1, kmax + 1)
    for a in [0.5, 1.5]:
        c = np.abs(gl_coefficients(a, kmax))[1:]
        ax.loglog(k, c, label=fr"$\alpha={a:g}$ (дробный)")
    c1 = np.abs(gl_coefficients(1.0, kmax))[1:]
    nz = c1 > 0
    ax.loglog(k[nz], c1[nz], "o", ms=7, label=r"$\alpha=1$ (один член)")
    c_inf = 1.0 / abs(gamma(-0.5))
    ax.loglog(k, c_inf * k ** (-1.5), "k--", lw=1, alpha=0.6,
              label=r"асимптотика $k^{-(\alpha+1)}/|\Gamma(-\alpha)|$, $\alpha=0.5$")
    ax.set_xlabel("k"); ax.set_ylabel(r"$|c_k|$")
    ax.set_title(r"Затухание коэффициентов $c_k$")
    ax.legend(fontsize=9)
    return _save(fig, "coeff_decay.png")


def power_frac():
    spec = fn.get("x2")
    xs = np.linspace(0.2, 5, 300)
    h = 0.01
    half = gl_grid_from_zero(spec.f, xs, 0.5, h)
    ref_half = spec.exact_frac(xs, 0.5)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, spec.f(xs), label=r"$x^2$ ($\alpha=0$)")
    ax.plot(xs, half, "C1", lw=2, label=r"$D^{0.5}$ (ГЛ)")
    ax.plot(xs, ref_half, "C1--", lw=1, label=r"$D^{0.5}$ (через $\Gamma$)")
    ax.plot(xs, 2 * xs, "C2:", label=r"$2x$ ($\alpha=1$)")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Дробная производная $x^2$")
    ax.legend(fontsize=9)
    return _save(fig, "power_frac.png")


def convergence():
    hs = np.array([0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625])
    spec_sin = fn.get("sin")
    err_sin = [abs(gl_point(spec_sin.f, 1.0, 1.0, h, 50) - np.cos(1.0)) for h in hs]
    spec_x2 = fn.get("x2")
    ref = float(spec_x2.exact_frac(np.array([2.0]), 0.5)[0])
    err_x2 = [abs(gl_point_from_zero(spec_x2.f, 2.0, 0.5, h) - ref) for h in hs]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.loglog(hs, err_sin, "o-", label=r"$\alpha=1$, $\sin x$, $x=1$")
    ax.loglog(hs, err_x2, "s-", label=r"$\alpha=0.5$, $x^2$, $x=2$")
    ax.loglog(hs, hs * (err_sin[0] / hs[0]), "k--", lw=1, alpha=0.6,
              label=r"$O(h)$")
    ax.set_xlabel(r"шаг $h$"); ax.set_ylabel("абсолютная ошибка")
    ax.set_title(r"Сходимость метода: ошибка $\sim O(h)$")
    ax.legend(fontsize=9)
    return _save(fig, "convergence.png")


def exp_orders(h=0.01, N=500):
    spec = fn.get("exp")
    xs = np.linspace(0, 3, 300)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for a in [0.0, 0.5, 1.0, 1.5, 2.0]:
        ax.plot(xs, gl_grid(spec.f, xs, a, h, N), label=fr"$\alpha={a:g}$")
    ax.plot(xs, np.exp(xs), "k--", lw=1, alpha=0.5, label=r"$e^x$")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Дробные производные $e^x$")
    ax.legend(fontsize=8, ncol=2)
    return _save(fig, "exp_orders.png")


def ln_orders(h=0.01, N=500):
    spec = fn.get("ln")
    xs = np.linspace(6, 10, 300)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, spec.f(xs), label=r"$\ln x$ ($\alpha=0$)")
    for a in [0.5, 1.0]:
        ax.plot(xs, gl_grid(spec.f, xs, a, h, N), label=fr"$\alpha={a:g}$")
    ax.plot(xs, 1.0 / xs, "k--", lw=1, alpha=0.6, label=r"$1/x$ ($\alpha=1$)")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"$\ln x$ на $[6,10]$ при условии $x-Nh>0$")
    ax.legend(fontsize=9)
    return _save(fig, "ln_orders.png")


def left_vs_right(h=0.01, N=500):
    spec = fn.get("sin")
    xs = np.linspace(np.pi, 3 * np.pi, 400)
    left = gl_grid(spec.f, xs, 0.5, h, N)
    right = gl_grid_right(spec.f, xs, 0.5, h, N)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, np.sin(xs), "k-", lw=1, alpha=0.5, label=r"$\sin x$")
    ax.plot(xs, left, "C0", lw=2, label=r"левая $D^{0.5}$")
    ax.plot(xs, right, "C3", lw=2, label=r"правая $D^{0.5}$")
    ax.plot(xs, np.sin(xs + np.pi / 4), "C0--", lw=1, label=r"$\sin(x+\pi/4)$")
    ax.plot(xs, np.sin(xs - np.pi / 4), "C3--", lw=1, label=r"$\sin(x-\pi/4)$")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Левая и правая $D^{0.5} \sin x$")
    ax.legend(fontsize=8, ncol=2)
    return _save(fig, "left_vs_right.png")


def atlas(h=0.01, N=500):
    spec = fn.get("sin")
    alphas = np.linspace(0, 2, 81)
    xs = np.linspace(0, 4 * np.pi, 300)
    M = ex.atlas_matrix("sin", alphas, xs, h, N)
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    im = ax.imshow(M, aspect="auto", origin="lower", cmap="RdBu_r",
                   extent=[xs[0], xs[-1], alphas[0], alphas[-1]],
                   vmin=-1.2, vmax=1.2)
    for a in [1.0, 2.0]:
        ax.axhline(a, color="k", lw=0.6, ls=":")
    ax.set_xlabel("x"); ax.set_ylabel(r"порядок $\alpha$")
    ax.set_title(r"Карта значений $D^{\alpha} \sin x$ (цвет - значение)")
    fig.colorbar(im, ax=ax, label="значение")
    ax.grid(False)
    return _save(fig, "atlas.png")


def rounding_floor():
    hs = np.logspace(-1, -12, 30)
    df = ex.rounding_floor("sin", 1, list(hs), x=1.0, N=2)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.loglog(df["h"], df["ошибка"], "o-", ms=4, label=r"ошибка $D^1 \sin x$, $x=1$")
    ax.loglog(hs, 0.42 * hs, "k--", lw=1, alpha=0.6, label=r"дискретизация $\sim h/2$")
    ax.loglog(hs, 1e-16 / hs, "r:", lw=1, alpha=0.7, label=r"округление $\sim \varepsilon/h$")
    ax.set_xlabel(r"шаг $h$"); ax.set_ylabel("абсолютная ошибка")
    ax.set_title(r"Порог округления: при очень малом $h$ ошибка снова растёт")
    ax.legend(fontsize=9)
    return _save(fig, "rounding_floor.png")


def richardson():
    hs = np.array([0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625])
    df = ex.richardson_convergence("sin", 1, list(hs), x=1.0, N=2)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.loglog(hs, df["ошибка (обычная)"], "o-", label=r"обычная схема, $O(h)$")
    ax.loglog(hs, df["ошибка (Ричардсон)"], "s-", label=r"Ричардсон, $O(h^2)$")
    ax.loglog(hs, hs * (df["ошибка (обычная)"].iloc[0] / hs[0]), "k--", lw=1,
              alpha=0.5, label=r"наклон 1")
    ax.loglog(hs, hs ** 2 * (df["ошибка (Ричардсон)"].iloc[0] / hs[0] ** 2),
              "k:", lw=1, alpha=0.5, label=r"наклон 2")
    ax.set_xlabel(r"шаг $h$"); ax.set_ylabel("абсолютная ошибка")
    ax.set_title(r"Экстраполяция Ричардсона, $\alpha=1$")
    ax.legend(fontsize=9)
    return _save(fig, "richardson.png")


def richardson_frac():
    hs = np.array([0.04, 0.02, 0.01, 0.005, 0.0025, 0.00125])
    df = ex.richardson_convergence_frac("x2", 0.5, list(hs), x=2.0)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.loglog(hs, df["ошибка (обычная)"], "o-", label=r"обычная схема, $O(h)$")
    ax.loglog(hs, df["ошибка (Ричардсон)"], "s-", label=r"Ричардсон, $O(h^2)$")
    ax.loglog(hs, hs * (df["ошибка (обычная)"].iloc[0] / hs[0]), "k--", lw=1,
              alpha=0.5, label=r"наклон 1")
    ax.loglog(hs, hs ** 2 * (df["ошибка (Ричардсон)"].iloc[0] / hs[0] ** 2),
              "k:", lw=1, alpha=0.5, label=r"наклон 2")
    ax.set_xlabel(r"шаг $h$"); ax.set_ylabel("абсолютная ошибка")
    ax.set_title(r"Экстраполяция Ричардсона для $D^{0.5} x^2$, $x=2$")
    ax.legend(fontsize=9)
    return _save(fig, "richardson_frac.png")


def N_truncation():
    spec = fn.get("sin")
    xs = np.linspace(np.pi, 3 * np.pi, 200)
    Ns = np.array([5, 10, 20, 50, 100, 200, 300, 500, 1000, 2000])
    ref = spec.exact_frac(xs, 0.5)
    errs = [float(np.nanmax(np.abs(gl_grid(spec.f, xs, 0.5, 0.01, N) - ref)))
            for N in Ns]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.loglog(Ns, errs, "o-", label=r"макс. ошибка $D^{0.5} \sin x$")
    ax.loglog(Ns, errs[0] * (Ns / Ns[0]) ** (-0.5), "k--", lw=1, alpha=0.6,
              label=r"оценка усечения $N^{-\alpha}$, $\alpha=0.5$")
    ax.set_xlabel(r"число членов $N$"); ax.set_ylabel("макс. ошибка")
    ax.set_title(r"Усечение истории: ошибка убывает быстрее $N^{-\alpha}$")
    ax.legend(fontsize=9)
    return _save(fig, "N_truncation.png")


def coeff_partial_sums(N=500):
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    n = np.arange(N + 1)
    for a in [0.25, 0.5, 0.75]:
        ax.plot(n, coefficient_partial_sums(a, N), label=fr"$\alpha={a:g}$")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("n"); ax.set_ylabel(r"$S_n$")
    ax.set_title(r"Частичные суммы коэффициентов $S_n \to 0$")
    ax.legend(fontsize=9)
    return _save(fig, "coeff_sums.png")


def error_heatmap():
    hs = np.array([0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
    Ns = np.array([10, 20, 50, 100, 200, 500, 1000])
    xs = np.linspace(np.pi, 3 * np.pi, 120)
    M = ex.error_grid_hN("sin", 1, hs, Ns, xs)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(np.log10(M), aspect="auto", origin="upper", cmap="viridis",
                   extent=[0, len(Ns), 0, len(hs)])
    ax.set_xticks(np.arange(len(Ns)) + 0.5); ax.set_xticklabels(Ns)
    ax.set_yticks(np.arange(len(hs)) + 0.5); ax.set_yticklabels(hs[::-1])
    ax.set_xlabel(r"$N$"); ax.set_ylabel(r"$h$")
    ax.set_title(r"$\log_{10}$ макс. ошибки $D^1 \sin x$ по сетке $(h, N)$")
    fig.colorbar(im, ax=ax, label=r"$\log_{10}$ ошибки")
    ax.grid(False)
    return _save(fig, "error_heatmap.png")


def error_heatmap_frac():
    hs = np.array([0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
    Ns = np.array([10, 20, 50, 100, 200, 500, 1000])
    xs = np.linspace(np.pi, 3 * np.pi, 120)
    M = ex.error_grid_hN_frac("sin", 0.5, hs, Ns, xs)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(np.log10(M), aspect="auto", origin="upper", cmap="viridis",
                   extent=[0, len(Ns), 0, len(hs)])
    ax.set_xticks(np.arange(len(Ns)) + 0.5); ax.set_xticklabels(Ns)
    ax.set_yticks(np.arange(len(hs)) + 0.5); ax.set_yticklabels(hs[::-1])
    ax.set_xlabel(r"$N$"); ax.set_ylabel(r"$h$")
    ax.set_title(r"$\log_{10}$ макс. ошибки $D^{0.5} \sin x$ по сетке $(h, N)$")
    fig.colorbar(im, ax=ax, label=r"$\log_{10}$ ошибки")
    ax.grid(False)
    return _save(fig, "error_heatmap_frac.png")


def tan_instability(h=0.01, N=100):
    spec = fn.get("tan")
    xs = np.linspace(0.2, 1.3, 300)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, spec.f(xs), label=r"$\tan x$")
    ax.plot(xs, gl_grid(spec.f, xs, 0.5, h, N), label=r"$D^{0.5}$")
    ax.plot(xs, gl_grid(spec.f, xs, 1.0, h, N), label=r"$D^1$ (ГЛ)")
    ax.plot(xs, 1.0 / np.cos(xs) ** 2, "k--", lw=1, alpha=0.6, label=r"$1/\cos^2 x$")
    ax.set_ylim(0, 15)
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"$\tan x$ на $[0.2, 1.3]$ около $\pi/2$")
    ax.legend(fontsize=9)
    return _save(fig, "tan_instability.png")


def x3_orders(h=0.01):
    spec = fn.get("x3")
    xs = np.linspace(0.3, 4, 300)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, spec.f(xs), label=r"$x^3$ ($\alpha=0$)")
    for a in [0.5, 1.0, 1.5, 2.0]:
        y = gl_grid_from_zero(spec.f, xs, a, h)
        ax.plot(xs, y, label=fr"$\alpha={a:g}$")
    ax.plot(xs, 6 * xs, "k--", lw=1, alpha=0.5, label=r"$6x$ ($\alpha=2$)")
    ax.set_ylim(-5, 65)
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Дробные производные $x^3$")
    ax.legend(fontsize=8, ncol=2)
    return _save(fig, "x3_orders.png")


def shifted_convergence(x=2.0):
    spec = fn.get("x2")
    exact = float(spec.exact_frac(np.array([x]), 0.5)[0])
    hs = np.array([0.04, 0.02, 0.01, 0.005, 0.0025])
    e_std = np.array([abs(gl_point_from_zero(spec.f, x, 0.5, h) - exact) for h in hs])
    e_sh = np.array([abs(gl_shifted_point_from_zero(spec.f, x, 0.5, h) - exact) for h in hs])
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.loglog(hs, e_std, "o-", label=r"стандартная ГЛ ($p=0$)")
    ax.loglog(hs, e_sh, "s-", label=r"сдвинутая ГЛ ($p=1$)")
    ax.loglog(hs, hs * (e_std[0] / hs[0]), "k--", lw=1, alpha=0.5, label=r"наклон $1$")
    ax.set_xlabel("шаг h"); ax.set_ylabel("ошибка")
    ax.set_title(r"Стандартная и сдвинутая ГЛ для $D^{0.5} x^2$")
    ax.legend(fontsize=9)
    return _save(fig, "shifted_convergence.png")


def gl_vs_caputo(alpha=0.5, h=0.005):
    spec = fn.get("exp")
    xs = np.linspace(0.3, 2.5, 200)
    gl = gl_grid_from_zero(spec.f, xs, alpha, h)
    cap = caputo_l1_grid(spec.f, xs, alpha, h)
    corr = xs ** (-alpha) / gamma(1.0 - alpha)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(xs, gl, label=r"Грюнвальд--Летников ($a=0$)")
    ax.plot(xs, cap, label=r"Капуто (L1)")
    ax.plot(xs, cap + corr, "k--", lw=1, alpha=0.6,
            label=r"Капуто $+\,x^{-\alpha}/\Gamma(1-\alpha)$")
    ax.set_xlabel("x"); ax.set_ylabel("значение")
    ax.set_title(r"Грюнвальд--Летников и Капуто для $D^{0.5} e^x$")
    ax.legend(fontsize=9)
    return _save(fig, "gl_vs_caputo.png")


def build_all():
    return [
        sin_orders(), alpha1_check(), h_influence(), N_influence(),
        coeff_decay(), power_frac(), convergence(), exp_orders(), ln_orders(),
        left_vs_right(), atlas(), rounding_floor(), richardson(),
        richardson_frac(), N_truncation(), coeff_partial_sums(),
        error_heatmap(), error_heatmap_frac(), tan_instability(), x3_orders(),
        shifted_convergence(), gl_vs_caputo(),
    ]


if __name__ == "__main__":
    for p in build_all():
        print("сохранён", p)
