import styles from "./AppHeader.module.scss";

export function AppHeader() {
  return (
    <header className={styles.header}>
      <div>
        <h1>Дробные производные Грюнвальда-Летникова</h1>
        <p>Расчёт значений, график и таблица для элементарных функций</p>
      </div>
    </header>
  );
}
