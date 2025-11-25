import TaskCard from "./TaskCard.js";
import * as taskUtils from "./taskUtils.js";

// const createTaskBtn = document.getElementById("create-task");
// Обработчик кнопки создания задач
export function setupCreateTaskButton(button) {
  if (!button) return;

  button.addEventListener("click", () => {
    if (!taskUtils.getTaskFlag()) {
      // Первый клик — создаем задачу
      new TaskCard();
      taskUtils.setTaskFlag(true); // включаем флаг
    } else {
      // Повторный клик — уведомление
      alert("Завершите создание задачи или отмените.");
    }
  });
}
