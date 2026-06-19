import type { MathFn } from "./types";

function grunwaldWeights(order: number, terms: number): number[] {
  const weights: number[] = [1];
  for (let k = 1; k <= terms; k += 1) {
    weights.push((weights[k - 1] * (k - 1 - order)) / k);
  }
  return weights;
}

function makeLeftDerivative(
  f: MathFn,
  order: number,
  step: number,
  terms: number,
  shift: number,
): (x: number) => number {
  const weights = grunwaldWeights(order, terms);
  const scale = step ** order;

  return (x) => {
    let total = 0;
    for (let k = 0; k < weights.length; k += 1) {
      const sample = f(x - (k - shift) * step);
      if (!Number.isFinite(sample)) {
        return Number.NaN;
      }
      total += weights[k] * sample;
    }
    return total / scale;
  };
}

export function glGrid(f: MathFn, xs: number[], alpha: number, h: number, n: number): number[] {
  return xs.map(makeLeftDerivative(f, alpha, h, n, 0));
}

export function glGridFromZero(f: MathFn, xs: number[], alpha: number, h: number): number[] {
  const positives = xs.filter((x) => x > 0);
  const nmax = positives.length > 0 ? Math.floor(Math.max(...positives) / h + 1e-12) : 0;
  const weights = grunwaldWeights(alpha, nmax);

  return xs.map((x) => {
    const n = Math.floor(x / h + 1e-12);
    if (n < 0) {
      return Number.NaN;
    }
    let total = 0;
    for (let k = 0; k <= n; k += 1) {
      const sample = f(x - k * h);
      if (!Number.isFinite(sample)) {
        return Number.NaN;
      }
      total += weights[k] * sample;
    }
    return total / h ** alpha;
  });
}

export function glShiftedGrid(
  f: MathFn,
  xs: number[],
  alpha: number,
  h: number,
  n: number,
  p = 1,
): number[] {
  return xs.map(makeLeftDerivative(f, alpha, h, n, p));
}

export function historyLength(h: number, n: number): number {
  return h * n;
}

function gamma(z: number): number {
  let reduction = 1;
  let w = z;
  while (w < 12) {
    reduction *= w;
    w += 1;
  }
  const inv = 1 / w;
  const stirling =
    (w - 0.5) * Math.log(w) -
    w +
    0.5 * Math.log(2 * Math.PI) +
    inv / 12 -
    inv ** 3 / 360 +
    inv ** 5 / 1260;
  return Math.exp(stirling) / reduction;
}

export function caputoL1Grid(f: MathFn, xs: number[], alpha: number, h: number): number[] {
  if (alpha <= 0 || alpha >= 1) {
    return xs.map(() => Number.NaN);
  }

  const stepCounts = xs.map((x) => (x > 0 ? Math.floor(x / h + 1e-12) : 0));
  const maxSteps = stepCounts.reduce((acc, value) => Math.max(acc, value), 0);

  const samples = Array.from({ length: maxSteps + 1 }, (_, j) => f(j * h));
  const weights = Array.from({ length: maxSteps + 1 }, (_, j) =>
    j >= 1 ? j ** (1 - alpha) - (j - 1) ** (1 - alpha) : 0,
  );
  const firstBad = samples.findIndex((value) => !Number.isFinite(value));
  const scale = gamma(2 - alpha) * h ** alpha;

  return xs.map((_, index) => {
    const steps = stepCounts[index];
    if (steps < 1 || (firstBad !== -1 && firstBad <= steps)) {
      return Number.NaN;
    }
    let total = 0;
    for (let j = 1; j <= steps; j += 1) {
      total += weights[j] * (samples[steps - j + 1] - samples[steps - j]);
    }
    return total / scale;
  });
}
