import type { FunctionSpec } from "./types";

export const FUNCTIONS: FunctionSpec[] = [
  {
    key: "one",
    label: "1",
    interval: [1, 5],
    note: "Постоянная: целая производная равна нулю, дробная — нет.",
    f: () => 1,
    classical: {
      1: () => 0,
      2: () => 0,
    },
  },
  {
    key: "x",
    label: "x",
    interval: [1, 5],
    f: (x) => x,
    classical: {
      1: () => 1,
      2: () => 0,
    },
  },
  {
    key: "x2",
    label: "x^2",
    interval: [1, 5],
    f: (x) => x ** 2,
    classical: {
      1: (x) => 2 * x,
      2: () => 2,
    },
  },
  {
    key: "x3",
    label: "x^3",
    interval: [1, 5],
    f: (x) => x ** 3,
    classical: {
      1: (x) => 3 * x ** 2,
      2: (x) => 6 * x,
    },
  },
  {
    key: "sin",
    label: "sin x",
    interval: [0, 4 * Math.PI],
    f: Math.sin,
    classical: {
      1: Math.cos,
      2: (x) => -Math.sin(x),
    },
  },
  {
    key: "cos",
    label: "cos x",
    interval: [0, 4 * Math.PI],
    f: Math.cos,
    classical: {
      1: (x) => -Math.sin(x),
      2: (x) => -Math.cos(x),
    },
  },
  {
    key: "exp",
    label: "e^x",
    interval: [0, 3],
    f: Math.exp,
    classical: {
      1: Math.exp,
      2: Math.exp,
    },
  },
  {
    key: "ln",
    label: "ln x",
    interval: [6, 10],
    note: "Для ln x вся история x-kh должна оставаться в области x>0.",
    f: (x) => (x > 0 ? Math.log(x) : Number.NaN),
    classical: {
      1: (x) => 1 / x,
      2: (x) => -1 / x ** 2,
    },
  },
  {
    key: "tan",
    label: "tan x",
    interval: [0.2, 1.3],
    note: "Интервал выбран в стороне от разрыва pi/2.",
    f: Math.tan,
    classical: {
      1: (x) => 1 / Math.cos(x) ** 2,
    },
  },
  {
    key: "xsin",
    label: "x*sin x",
    interval: [0, 4 * Math.PI],
    f: (x) => x * Math.sin(x),
    classical: {
      1: (x) => Math.sin(x) + x * Math.cos(x),
      2: (x) => 2 * Math.cos(x) - x * Math.sin(x),
    },
  },
  {
    key: "xexp",
    label: "x*e^x",
    interval: [0, 3],
    f: (x) => x * Math.exp(x),
    classical: {
      1: (x) => Math.exp(x) * (1 + x),
      2: (x) => Math.exp(x) * (2 + x),
    },
  },
  {
    key: "sin_plus_cos",
    label: "sin x + cos x",
    interval: [0, 4 * Math.PI],
    f: (x) => Math.sin(x) + Math.cos(x),
    classical: {
      1: (x) => Math.cos(x) - Math.sin(x),
      2: (x) => -Math.sin(x) - Math.cos(x),
    },
  },
];

export function getFunctionSpec(key: string): FunctionSpec {
  const spec = FUNCTIONS.find((item) => item.key === key);
  if (!spec) {
    throw new Error(`Неизвестная функция: ${key}`);
  }
  return spec;
}
