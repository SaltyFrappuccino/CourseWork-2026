import { AuthorBadge } from "./components/AuthorBadge/AuthorBadge";
import { AppHeader } from "./components/AppHeader/AppHeader";
import { ChartPanel } from "./components/ChartPanel/ChartPanel";
import { ControlsPanel } from "./components/ControlsPanel/ControlsPanel";
import { DataTable } from "./components/DataTable/DataTable";
import { MethodNotes } from "./components/MethodNotes/MethodNotes";
import { downloadCsv } from "./domain/csv";
import { makeCsvRows } from "./domain/derivativeModel";
import { useCalculatorState } from "./hooks/useCalculatorState";
import { useDerivativeModel } from "./hooks/useDerivativeModel";
import styles from "./App.module.scss";

export default function App() {
  const calculator = useCalculatorState("sin");
  const model = useDerivativeModel(calculator.settings);

  function handleCsvDownload() {
    downloadCsv(`${calculator.settings.spec.key}_a_${calculator.settings.alpha}.csv`, makeCsvRows(model));
  }

  return (
    <main className={styles.shell}>
      <AppHeader />
      <section className={styles.workspace} aria-label="Расчёт дробной производной">
        <ControlsPanel calculator={calculator} onCsvDownload={handleCsvDownload} />
        <ChartPanel settings={calculator.settings} model={model} />
        <DataTable settings={calculator.settings} model={model} />
      </section>
      <MethodNotes />
      <AuthorBadge />
    </main>
  );
}
