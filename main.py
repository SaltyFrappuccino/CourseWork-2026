import argparse

import numpy as np
import pandas as pd

import functions as fn
from fractional import gl_point, gl_grid


def run_all():
    import tables
    import plots
    tabs = tables.build_all()
    print("Таблицы сохранены в tables/ (CSV + tables.xlsx):")
    for name in tabs:
        print("  -", name)
    for p in plots.build_all():
        print("график:", p)


def main():
    p = argparse.ArgumentParser(description="Дробная производная Грюнвальда-Летникова")
    p.add_argument("--all", action="store_true")
    p.add_argument("--function", default="sin", help=f"одна из: {', '.join(fn.names())}")
    p.add_argument("--alpha", type=float, default=0.5)
    p.add_argument("--h", type=float, default=0.01)
    p.add_argument("--n", type=int, default=500)
    p.add_argument("--x", type=float, default=None)
    p.add_argument("--xmin", type=float, default=None)
    p.add_argument("--xmax", type=float, default=None)
    p.add_argument("--points", type=int, default=9)
    p.add_argument("--csv", default=None)
    args = p.parse_args()

    if args.all:
        run_all()
        return

    spec = fn.get(args.function)
    if args.x is not None:
        value = gl_point(spec.f, args.x, args.alpha, args.h, args.n)
        print(f"D^{args.alpha:g} [{spec.label}] (x={args.x:g}) = {value:.6f}")
        if args.csv:
            df = pd.DataFrame({"x": [args.x], "f(x)": [float(spec.f(np.array([args.x]))[0])],
                               f"D^{args.alpha:g}": [value]})
            df.to_csv(args.csv, index=False, encoding="utf-8-sig")
            print("сохранено в", args.csv)
        return

    xmin = args.xmin if args.xmin is not None else spec.interval[0]
    xmax = args.xmax if args.xmax is not None else spec.interval[1]
    xs = np.linspace(xmin, xmax, args.points)
    y = gl_grid(spec.f, xs, args.alpha, args.h, args.n)
    df = pd.DataFrame({"x": xs, "f(x)": spec.f(xs), f"D^{args.alpha:g}": y})
    print(df.to_string(index=False))
    if args.csv:
        df.to_csv(args.csv, index=False, encoding="utf-8-sig")
        print("сохранено в", args.csv)


if __name__ == "__main__":
    main()
