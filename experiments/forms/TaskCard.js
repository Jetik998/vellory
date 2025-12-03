// import * as taskUtils from "../../app/web/static/js/taskUtils.js";
//
// // Класс задачи
// export default class TaskCard {
//   constructor(id, title, description, completed, created_at, priority) {
//     this.id = id; // уникальный идентификатор задачи
//     this.title = title; // заголовок
//     this.description = description; // описание
//     this.completed = completed; // выполнена ли задача
//     this.created_at = created_at; // дата создания
//     this.priority = priority; // приоритет: число от 0 до 3
//
//     // Клонируем шаблон карточки, чтобы создать новую
//     this.card = template.cloneNode(true);
//     // Присваиваем уникальный id элементу карточки
//     this.card.id = `task-${this.id}`;
//     // Делаем карточку видимой (по умолчанию, возможно, скрыта в шаблоне)
//     this.card.style.display = "flex";
//     this.saveHandler = this.save.bind(this);
//     this.cancelHandler = this.cancel.bind(this);
//     this.priorityHandlers = []; // для кругов приоритета
//     // Устанавливаем номер задачи на карточке
//     this.setTaskNumber();
//     // Настраиваем кнопку сохранения
//     this.setupSaveButton();
//     // Настраиваем кнопку отмены
//     this.setupCancelButton();
//     // Настраиваем обработку кликов по кругам приоритетов
//     this.setupPriorityCircles();
//
//     // Добавляем новую карточку в контейнер на странице
//     container.appendChild(this.card);
//   }
//
//   // Метод для отображения номера задачи
//   setTaskNumber() {
//     const numberSpan = this.card.querySelector(".task-number");
//     if (numberSpan) numberSpan.textContent = `#${this.id}`;
//   }
//
//   // Метод для настройки кнопки "Сохранить"
//   setupSaveButton() {
//     this.card
//       .querySelector(".card-btn-save")
//       .addEventListener("click", this.saveHandler);
//   }
//   setupCancelButton() {
//     this.card
//       .querySelector(".card-btn-cancel")
//       .addEventListener("click", this.cancelHandler);
//   }
//
//   // Метод для настройки кликов по кругам приоритетов
//   setupPriorityCircles() {
//     const circles = this.card.querySelectorAll(".circle");
//     circles.forEach((circle, index) => {
//       const handler = () => this.togglePriority(circles, index); // сохраняем функцию в переменную
//       circle.addEventListener("click", handler); // навешиваем обработчик
//       this.priorityHandlers[index] = handler; // сохраняем ссылку для удаления
//     });
//   }
//
//   // Метод для изменения приоритета задачи при клике на круг
//   togglePriority(circles, index) {
//     const circle = circles[index];
//     const isActive = circle.classList.contains("active");
//
//     // Если круг не активен, активируем все до выбранного включительно
//     // Если уже активен, сбрасываем приоритет
//     circles.forEach((c, i) => {
//       if (!isActive && i <= index) {
//         c.classList.remove("active"); // На всякий случай сбрасываем класс
//         c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
//         circle.classList.add("active"); // Активируем выбранный круг
//       } else {
//         c.classList.remove("active"); // Деактивируем все остальные
//         c.style.backgroundColor = "transparent"; // Сброс цвета
//       }
//     });
//
//     // Сохраняем текущий уровень приоритета
//     this.taskPriority = isActive ? 0 : index + 1;
//     // console.log(`Task #${this.id} priority:`, this.taskPriority);
//   }
//
//   // Метод для "сохранения" задачи
//   save() {
//     // Делаем все поля ввода и textarea неактивными
//     this.card
//       .querySelectorAll("input, textarea")
//       .forEach((el) => (el.disabled = true));
//     // Делаем круги приоритетов некликабельными
//     this.card
//       .querySelectorAll(".circle")
//       .forEach((el) => (el.style.pointerEvents = "none"));
//     // Деактивируем кнопку сохранения
//     this.card
//       .querySelectorAll(".card-btn")
//       .forEach((btn) => (btn.style.display = "none"));
//     // Увеличить счетчик
//     taskUtils.incrementTaskId();
//     // Cброса флага состояния создания задачи
//     taskUtils.resetTaskFlag();
//   }
//
//   cancel() {
//     // Удаляем карточку из DOM
//     // 1. Снять все обработчики
//     this.card
//       .querySelector(".card-btn-save")
//       ?.removeEventListener("click", this.saveHandler);
//     this.card
//       .querySelector(".card-btn-cancel")
//       ?.removeEventListener("click", this.cancelHandler);
//     this.card.querySelectorAll(".circle").forEach((circle, index) => {
//       circle.removeEventListener("click", this.priorityHandlers[index]);
//     });
//
//     // 2. Удалить элемент из DOM
//     this.card.remove();
//
//     // 3. Обнулить ссылки
//     this.card = null;
//     this.saveHandler = null;
//     this.cancelHandler = null;
//     this.priorityHandlers = null;
//     // Cброса флага состояния создания задачи
//     taskUtils.resetTaskFlag();
//   }
// }
