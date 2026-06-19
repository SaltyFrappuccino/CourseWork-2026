export type MathFn = (x: number) => number;

export type ClassicalOrder = 0 | 1 | 2;

export type Scheme = "standard" | "fromZero" | "shifted" | "caputo";

export type FunctionSpec = {
  key: string;
  label: string;
  interval: [number, number];
  note?: string;
  f: MathFn;
  classical: Partial<Record<ClassicalOrder, MathFn>>;
};

export type CalculatorSettings = {
  spec: FunctionSpec;
  scheme: Scheme;
  alpha: number;
  h: number;
  n: number;
  xmin: number;
  xmax: number;
};

export type TableRow = {
  x: number;
  fx: number;
  derivative: number;
  exact?: number;
};
