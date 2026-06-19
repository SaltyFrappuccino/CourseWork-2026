import { expect, test } from "bun:test";

import { glGrid, glGridFromZero } from "./fractional";

test("alpha=0 возвращает саму функцию", () => {
  const xs = [0.5, 1.0, 1.5, 2.0];
  const got = glGrid(Math.sin, xs, 0, 0.01, 500);
  got.forEach((v, i) => expect(Math.abs(v - Math.sin(xs[i]))).toBeLessThan(1e-9));
});

test("alpha=2 для x^2 даёт ровно 2", () => {
  const got = glGrid((x) => x * x, [2.3], 2, 0.01, 500)[0];
  expect(Math.abs(got - 2)).toBeLessThan(1e-9);
});

test("D^0.5 x^2 (a=0) совпадает с Г-формулой (как в Python)", () => {
  const got = glGridFromZero((x) => x * x, [2.0], 0.5, 0.005)[0];
  expect(Math.abs(got - 4.255384)).toBeLessThan(0.01);
});

test("alpha=1 для sin x приближает cos x", () => {
  const got = glGrid(Math.sin, [1.0], 1, 0.01, 2)[0];
  expect(Math.abs(got - Math.cos(1.0))).toBeLessThan(0.01);
});
