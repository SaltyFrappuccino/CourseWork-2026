import styles from "./AuthorBadge.module.scss";

export function AuthorBadge() {
  return (
    <aside className={styles.badge} aria-label="Автор работы">
      <span>Выполнил</span>
      {" "}
      <strong>Шестак Александр Сергеевич</strong>
    </aside>
  );
}
