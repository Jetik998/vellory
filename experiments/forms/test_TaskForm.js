// // Класс задачи
// import * as taskUtils from "../app/web/static/js/taskUtils.js";
//
// export default class Test_TaskForm {
//   constructor(template) {
//     // Шаблон формы
//     this.template = template;
//     // Ссылка на текущий экземпляр
//     this.form = this.getCopy();
//     // Заголовок для задачи
//     this.title = this.form.querySelector(".card-title-input");
//     // Описание для задачи
//     this.description = this.form.querySelector(".card-content-input");
//     // Приоритет задачи
//     this.priority = 0;
//     // Привязываем метод save к this
//     this.saveHandler = this.save.bind(this);
//     // Привязываем метод cancel к this
//     this.cancelHandler = this.cancel.bind(this);
//     // Настраиваем кнопку "Сохранить"
//     this.setupSaveButton();
//     // Настраиваем кнопку "Отменить"
//     this.setupCancelButton();
//     this.setupPriorityCircles();
//     this.view();
//   }
//
//   getCopy() {
//     return this.template.cloneNode(true);
//   }
//
//   // Метод для настройки кнопки "Сохранить"
//   setupSaveButton() {
//     this.form
//       .querySelector(".card-btn-save")
//       .addEventListener("click", this.saveHandler);
//   }
//
//   // Метод для настройки кнопки "Отменить"
//   setupCancelButton() {
//     this.form
//       .querySelector(".card-btn-cancel")
//       .addEventListener("click", this.cancelHandler);
//   }
//
//   // Сохранить задачу
//   async save() {
//     const requestBody = {
//       title: this.title.value,
//       description: this.description.value,
//       completed: false,
//       priority: this.priority,
//     };
//
//     console.log(requestBody);
//     // Скрываем форму
//     this.cancel();
//     // Отправка запроса на регистрацию
//     try {
//       const response = await fetch("/tasks/create_task", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(requestBody),
//         credentials: "include",
//       });
//       const data = await response.json();
//       console.log(data);
//     } catch {
//       alert("Ошибка соединения с сервером");
//     }
//   }
//
//   // Отменить создание задачи и убрать с экрана
//   cancel() {
//     // Очищаем поля формы
//     this.title.value = "";
//     this.description.value = "";
//     this.priority = 0;
//
//     // Скрываем форму (можно через display: none)
//     this.form.style.display = "none";
//     taskUtils.setTaskFlag(false);
//   }
//
//   // Показать форму
//   view() {
//     this.form.style.display = "flex";
//   }
//
//   // Метод для настройки кликов по кругам приоритетов
//   setupPriorityCircles() {
//     // Ищет внутри карточки задачи все элементы с классом .circle.
//     const circles = this.form.querySelectorAll(".circle");
//     // Проходим по каждому кругу и назначаем обработчик клика.
//     circles.forEach((circle, index) => {
//       // Создаём функцию, которая при клике будет вызывать метод togglePriority и передавать: все круги (circles), индекс текущего круга (index)
//       const handler = () => this.activatePriorityCircles(circles, index);
//
//       // Сохраняем выбранный приоритет
//       this.priority = index;
//       // Привязываем обработчик клика к кругу.
//       circle.addEventListener("click", handler);
//     });
//   }
//
//   // Метод для изменения приоритета задачи при клике на круг
//   activatePriorityCircles(circles, index) {
//     // Выбранный круг, на который кликнули.
//     const circle = circles[index];
//     // Флаг нажат ли круг. 1 нажатие true второе false
//     const isActive = circle.classList.contains("active");
//     // c - текущий круг i - его индекс circles - все круги
//     // Если круг был нажат / isActive = true, делаем все круги прозрачными
//     // Иначе / isActive = false, в цикле для всех кругов до нажатого включительно, устанавливаем цвет.
//     // !Сбрасываем флаг active у всех, тк если флаг 2 = true то при нажатии флага 3
//     // информация о состоянии флага 2 уже не нужна.
//     circles.forEach((c, i) => {
//       if (!isActive && i <= index) {
//         c.classList.remove("active"); // Сбрасываем флаг у всех
//         c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
//         circle.classList.add("active"); // Активируем выбранный круг
//       } else {
//         c.classList.remove("active"); // Деактивируем все остальные
//         c.style.backgroundColor = "transparent"; // Сброс цвета
//       }
//     });
//   }
// }
