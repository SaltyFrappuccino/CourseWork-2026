export function downloadCsv(fileName: string, rows: Array<Record<string, string | number | undefined>>) {
  const headers = Object.keys(rows[0] ?? {});
  const csv = [
    headers.join(";"),
    ...rows.map((row) =>
      headers
        .map((key) => {
          const value = row[key];
          return value === undefined ? "" : String(value).replaceAll(".", ",");
        })
        .join(";"),
    ),
  ].join("\n");

  const blob = new Blob([`\ufeff${csv}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
}
