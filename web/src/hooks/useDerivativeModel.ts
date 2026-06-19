import { useMemo } from "react";
import { buildDerivativeModel } from "../domain/derivativeModel";
import type { CalculatorSettings } from "../domain/types";

export function useDerivativeModel(settings: CalculatorSettings) {
  return useMemo(
    () => buildDerivativeModel(settings),
    [
      settings.scheme,
      settings.alpha,
      settings.h,
      settings.n,
      settings.spec,
      settings.xmax,
      settings.xmin,
    ],
  );
}
