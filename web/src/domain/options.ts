import type { Scheme } from "./types";

export const H_OPTIONS = [0.1, 0.05, 0.02, 0.01, 0.005, 0.001];

export const SCHEME_OPTIONS: { value: Scheme; label: string }[] = [
  { value: "standard", label: "Грюнвальд-Летников" },
  { value: "fromZero", label: "ГЛ, нижний предел a=0" },
  { value: "shifted", label: "Сдвинутая ГЛ (p=1)" },
  { value: "caputo", label: "Капуто (L1)" },
];

export const POINT_COUNT = 360;

export const TABLE_STEP = 20;

export const ALPHA_RANGE = { min: 0, max: 2 };

export const CAPUTO_ALPHA_RANGE = { min: 0.05, max: 0.95 };
