import { InteractiveChart } from "../InteractiveChart/InteractiveChart";
import { formatNumber, formatOrder } from "../../domain/format";
import type { DerivativeModel } from "../../domain/derivativeModel";
import type { CalculatorSettings } from "../../domain/types";
import styles from "./ChartPanel.module.scss";

type Props = {
  settings: CalculatorSettings;
  model: DerivativeModel;
};

export function ChartPanel({ settings, model }: Props) {
  const errorText = model.error.value === null ? "не считается" : formatNumber(model.error.value, 6);

  return (
    <section className={styles.panel}>
      <div className={styles.heading}>
        <div>
          <h2>{settings.spec.label}</h2>
          <p>
            D^{formatOrder(settings.alpha)} при h={settings.h}, N={settings.n}
          </p>
        </div>
        <div className={styles.errorBox}>
          <span>Оценка отклонения</span>
          <strong>{errorText}</strong>
          <small>Сравнение с эталоном доступно только для α=0, 1, 2.</small>
        </div>
      </div>

      <InteractiveChart model={model} />
    </section>
  );
}
