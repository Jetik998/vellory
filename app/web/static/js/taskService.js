import * as taskUtils from "./taskUtils.js";

/**
 * Настраивает обработчик клика для кнопки создания задачи.
 *
 * При первом клике отображает форму создания задачи и устанавливает флаг активности.
 * Если флаг уже установлен (создание задачи в процессе), выводится предупреждение.
 *
 * @param {HTMLElement} button - Кнопка, на которую будет навешан обработчик клика.
 * @param {Object} taskForm - Объект формы задачи с методом `view()`, который отображает форму.
 */

export function setupCreateTask(button, taskForm) {
  if (!button) return;

  button.addEventListener("click", () => {
    if (!taskUtils.getTaskFlag()) {
      // Если состояние создания задачи не активно, отображаем форму
      taskForm.view();
      taskUtils.setTaskFlag(true); // Устанавливаем флаг
    } else {
      // Повторный клик — уведомление
      alert("Завершите создание задачи или отмените.");
    }
  });
}
