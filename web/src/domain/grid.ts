export function linspace(min: number, max: number, count: number): number[] {
  if (count <= 1) {
    return [min];
  }

  const step = (max - min) / (count - 1);
  return Array.from({ length: count }, (_, index) => min + index * step);
}
