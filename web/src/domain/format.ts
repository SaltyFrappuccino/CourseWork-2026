export function formatNumber(value: number, digits = 5): string {
  if (!Number.isFinite(value)) {
    return "не число";
  }

  if (Math.abs(value) >= 1000 || (Math.abs(value) > 0 && Math.abs(value) < 0.001)) {
    return value.toExponential(2).replace(".", ",");
  }

  return value.toLocaleString("ru-RU", {
    maximumFractionDigits: digits,
  });
}

export function formatFixed(value: number, digits = 2): string {
  return value.toLocaleString("ru-RU", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

export function formatOrder(value: number): string {
  return formatFixed(value, 2);
}
