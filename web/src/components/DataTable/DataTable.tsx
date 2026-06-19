import { formatNumber, formatOrder } from "../../domain/format";
import type { DerivativeModel } from "../../domain/derivativeModel";
import type { CalculatorSettings } from "../../domain/types";
import styles from "./DataTable.module.scss";

type Props = {
  settings: CalculatorSettings;
  model: DerivativeModel;
};

export function DataTable({ settings, model }: Props) {
  return (
    <aside className={styles.panel}>
      <div className={styles.heading}>
        <h2>Таблица</h2>
        <p>Показана каждая двадцатая точка сетки.</p>
      </div>
      <div className={styles.tableWrap}>
        <table>
          <thead>
            <tr>
              <th>x</th>
              <th>f(x)</th>
              <th>D^{formatOrder(settings.alpha)}</th>
              {model.classicalOrder !== null ? <th>Эталон</th> : null}
            </tr>
          </thead>
          <tbody>
            {model.rows.map((row) => (
              <tr key={row.x}>
                <td>{formatNumber(row.x, 4)}</td>
                <td>{formatNumber(row.fx, 4)}</td>
                <td>{formatNumber(row.derivative, 4)}</td>
                {model.classicalOrder !== null ? <td>{formatNumber(row.exact ?? Number.NaN, 4)}</td> : null}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </aside>
  );
}
