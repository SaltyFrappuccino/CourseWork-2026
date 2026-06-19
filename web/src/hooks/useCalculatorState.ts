import { useState } from "react";
import { getFunctionSpec } from "../domain/functions";
import { CAPUTO_ALPHA_RANGE } from "../domain/options";
import type { CalculatorSettings, Scheme } from "../domain/types";

function clampAlphaForScheme(value: number, scheme: Scheme): number {
  if (scheme !== "caputo") {
    return value;
  }
  return Math.min(CAPUTO_ALPHA_RANGE.max, Math.max(CAPUTO_ALPHA_RANGE.min, value));
}

export type CalculatorState = {
  settings: CalculatorSettings;
  setFunctionKey: (key: string) => void;
  setScheme: (value: Scheme) => void;
  setAlpha: (value: number) => void;
  setH: (value: number) => void;
  setN: (value: number) => void;
  setXmin: (value: number) => void;
  setXmax: (value: number) => void;
};

export function useCalculatorState(initialFunctionKey: string): CalculatorState {
  const [functionKey, setFunctionKeyState] = useState(initialFunctionKey);
  const [scheme, setSchemeState] = useState<Scheme>("standard");
  const [alpha, setAlpha] = useState(0.5);
  const [h, setH] = useState(0.01);
  const [n, setN] = useState(500);
  const [xmin, setXmin] = useState(() => getFunctionSpec(initialFunctionKey).interval[0]);
  const [xmax, setXmax] = useState(() => getFunctionSpec(initialFunctionKey).interval[1]);
  const spec = getFunctionSpec(functionKey);

  function setFunctionKey(key: string) {
    const nextSpec = getFunctionSpec(key);
    setFunctionKeyState(key);
    setXmin(nextSpec.interval[0]);
    setXmax(nextSpec.interval[1]);
  }

  function setScheme(next: Scheme) {
    setSchemeState(next);
    setAlpha((current) => clampAlphaForScheme(current, next));
  }

  return {
    settings: {
      spec,
      scheme,
      alpha,
      h,
      n,
      xmin,
      xmax,
    },
    setFunctionKey,
    setScheme,
    setAlpha,
    setH,
    setN,
    setXmin,
    setXmax,
  };
}
