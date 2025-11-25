let createTaskButtonClicked = false;

// Устанавливает флаг
export function setTaskFlag(value) {
  createTaskButtonClicked = value; // просто присваиваем значение
}

// Функция для просто получения текущего значения флага
export function getTaskFlag() {
  return createTaskButtonClicked;
}

// Пример сброса флага где-то в коде
export function resetTaskFlag() {
  createTaskButtonClicked = false;
}

let taskCounter = 1;

// Функция возвращает текущий последний ID без изменения счётчика
export function getCurrentTaskId() {
  return taskCounter;
}

// Функция увеличивает счётчик и возвращает новый ID
export function incrementTaskId() {
  return taskCounter++;
}
