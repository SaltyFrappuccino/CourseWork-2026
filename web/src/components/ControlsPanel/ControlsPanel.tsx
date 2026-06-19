import { FUNCTIONS } from "../../domain/functions";
import { historyLength } from "../../domain/fractional";
import { formatFixed, formatNumber } from "../../domain/format";
import { ALPHA_RANGE, CAPUTO_ALPHA_RANGE, H_OPTIONS, SCHEME_OPTIONS } from "../../domain/options";
import type { Scheme } from "../../domain/types";
import type { CalculatorState } from "../../hooks/useCalculatorState";
import styles from "./ControlsPanel.module.scss";

type Props = {
  calculator: CalculatorState;
  onCsvDownload: () => void;
};

export function ControlsPanel({ calculator, onCsvDownload }: Props) {
  const { settings } = calculator;
  const alphaRange = settings.scheme === "caputo" ? CAPUTO_ALPHA_RANGE : ALPHA_RANGE;
  const usesN = settings.scheme === "standard" || settings.scheme === "shifted";

  return (
    <aside className={styles.panel}>
      <div className={styles.titleRow}>
        <span>Параметры</span>
        <strong>{usesN ? `L = ${formatNumber(historyLength(settings.h, settings.n), 3)}` : "история до 0"}</strong>
      </div>

      <label className={styles.field}>
        Функция
        <select value={settings.spec.key} onChange={(event) => calculator.setFunctionKey(event.target.value)}>
          {FUNCTIONS.map((item) => (
            <option key={item.key} value={item.key}>
              {item.label}
            </option>
          ))}
        </select>
      </label>

      <label className={styles.field}>
        Схема
        <select value={settings.scheme} onChange={(event) => calculator.setScheme(event.target.value as Scheme)}>
          {SCHEME_OPTIONS.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
      </label>

      {settings.scheme === "caputo" ? (
        <p className={styles.note}>Схема Капуто (L1) определена для порядка 0 &lt; α &lt; 1 и нижнего предела 0.</p>
      ) : null}

      {settings.scheme === "fromZero" ? (
        <p className={styles.note}>
          Нижний предел a=0: число членов задаётся автоматически как N=⌊x/h⌋. На степенных функциях
          значения совпадают с формулой через Γ.
        </p>
      ) : null}

      <label className={styles.field}>
        Порядок α: {formatFixed(settings.alpha, 2)}
        <input
          type="range"
          min={alphaRange.min}
          max={alphaRange.max}
          step="0.05"
          value={settings.alpha}
          onChange={(event) => calculator.setAlpha(Number(event.target.value))}
        />
      </label>

      <label className={styles.field}>
        Шаг h
        <select value={settings.h} onChange={(event) => calculator.setH(Number(event.target.value))}>
          {H_OPTIONS.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </label>

      <label className={styles.field}>
        Число членов N: {usesN ? settings.n : "—"}
        <input
          type="range"
          min="10"
          max="1000"
          step="10"
          value={settings.n}
          disabled={!usesN}
          onChange={(event) => calculator.setN(Number(event.target.value))}
        />
      </label>

      <div className={styles.bounds}>
        <label className={styles.field}>
          Левая граница
          <input
            type="number"
            value={settings.xmin}
            step="0.1"
            onChange={(event) => calculator.setXmin(Number(event.target.value))}
          />
        </label>
        <label className={styles.field}>
          Правая граница
          <input
            type="number"
            value={settings.xmax}
            step="0.1"
            onChange={(event) => calculator.setXmax(Number(event.target.value))}
          />
        </label>
      </div>

      {settings.spec.note ? <p className={styles.note}>{settings.spec.note}</p> : null}

      <button className={styles.downloadButton} type="button" onClick={onCsvDownload}>
        Скачать CSV
      </button>
    </aside>
  );
}
