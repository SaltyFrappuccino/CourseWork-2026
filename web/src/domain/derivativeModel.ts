import { glGrid, glGridFromZero, glShiftedGrid, caputoL1Grid } from "./fractional";
import { formatOrder } from "./format";
import { linspace } from "./grid";
import { POINT_COUNT, TABLE_STEP } from "./options";
import type { CalculatorSettings, ClassicalOrder, Scheme, TableRow } from "./types";

const SCHEME_SHORT: Record<Scheme, string> = {
  standard: "ГЛ",
  fromZero: "ГЛ a=0",
  shifted: "сдвиг",
  caputo: "Капуто",
};

function computeDerivative(settings: CalculatorSettings, xs: number[]): number[] {
  switch (settings.scheme) {
    case "fromZero":
      return glGridFromZero(settings.spec.f, xs, settings.alpha, settings.h);
    case "shifted":
      return glShiftedGrid(settings.spec.f, xs, settings.alpha, settings.h, settings.n, 1);
    case "caputo":
      return caputoL1Grid(settings.spec.f, xs, settings.alpha, settings.h);
    default:
      return glGrid(settings.spec.f, xs, settings.alpha, settings.h, settings.n);
  }
}

export type ChartSeries = {
  name: string;
  color: string;
  dashed?: boolean;
  strokeWidth?: number;
  values: number[];
};

export type DerivativeModel = {
  xs: number[];
  rows: TableRow[];
  series: ChartSeries[];
  classicalOrder: ClassicalOrder | null;
  error: {
    value: number | null;
    sampleCount: number;
  };
};

export function buildDerivativeModel(settings: CalculatorSettings): DerivativeModel {
  const xmin = Math.min(settings.xmin, settings.xmax);
  const xmax = Math.max(settings.xmin, settings.xmax);
  const xs = linspace(xmin, xmax, POINT_COUNT);
  const functionValues = xs.map(settings.spec.f);
  const derivativeValues = computeDerivative(settings, xs);
  const classicalOrder = getClassicalOrder(settings.alpha);
  const exactFn =
    classicalOrder === null
      ? undefined
      : classicalOrder === 0
        ? settings.spec.f
        : settings.spec.classical[classicalOrder];
  const exactValues = exactFn ? xs.map(exactFn) : [];
  const rows = makeRows(xs, functionValues, derivativeValues, exactValues);
  const series = makeSeries(settings, functionValues, derivativeValues, exactValues, classicalOrder);

  return {
    xs,
    rows,
    series,
    classicalOrder,
    error: calculateAbsoluteError(derivativeValues, exactValues),
  };
}

export function makeCsvRows(model: DerivativeModel): Array<Record<string, string | number | undefined>> {
  return model.rows.map((row) => ({
    x: row.x,
    "f(x)": row.fx,
    "D^α f(x)": row.derivative,
    "эталон": row.exact,
  }));
}

function getClassicalOrder(alpha: number): ClassicalOrder | null {
  const rounded = Math.round(alpha);
  if (Math.abs(alpha - rounded) > 1e-9) {
    return null;
  }

  if (rounded === 0 || rounded === 1 || rounded === 2) {
    return rounded;
  }

  return null;
}

function calculateAbsoluteError(values: number[], exactValues: number[]) {
  let max = 0;
  let sampleCount = 0;

  values.forEach((value, index) => {
    const exact = exactValues[index];
    if (!Number.isFinite(value) || !Number.isFinite(exact)) {
      return;
    }

    max = Math.max(max, Math.abs(value - exact));
    sampleCount += 1;
  });

  return {
    value: sampleCount === 0 ? null : max,
    sampleCount,
  };
}

function makeRows(xs: number[], fValues: number[], derivativeValues: number[], exactValues: number[]): TableRow[] {
  return xs
    .filter((_, index) => index % TABLE_STEP === 0)
    .map((x, rowIndex) => {
      const sourceIndex = rowIndex * TABLE_STEP;
      return {
        x,
        fx: fValues[sourceIndex],
        derivative: derivativeValues[sourceIndex],
        exact: exactValues[sourceIndex],
      };
    });
}

function makeSeries(
  settings: CalculatorSettings,
  functionValues: number[],
  derivativeValues: number[],
  exactValues: number[],
  classicalOrder: ClassicalOrder | null,
): ChartSeries[] {
  const series: ChartSeries[] = [
    {
      name: `${settings.spec.label}, α=0`,
      color: "#60727a",
      dashed: true,
      values: functionValues,
    },
    {
      name: `D^${formatOrder(settings.alpha)} (${SCHEME_SHORT[settings.scheme]})`,
      color: "#087b7b",
      strokeWidth: 3,
      values: derivativeValues,
    },
  ];

  if (exactValues.length > 0) {
    series.push({
      name: `эталон D^${classicalOrder}`,
      color: "#a86805",
      dashed: true,
      values: exactValues,
    });
  }

  return series;
}
