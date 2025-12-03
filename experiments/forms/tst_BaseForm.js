// export class Tst_BaseForm {
//   constructor(template) {
//     this.form = template;
//     this.title = this.form.querySelector(".card-title-input");
//     this.description = this.form.querySelector(".card-content-input");
//     this.priority = 0;
//     this.saveBtn = this.form.querySelector(".card-btn-save");
//     this.cancelBtn = this.form.querySelector(".card-btn-cancel");
//
//
//     this.setupPriorityCircles();
//   }
//
//     // Метод для очистки полей
//     clearFields() {
//         this.title.value = "";
//         this.description.value = "";
//         this.priority = 0;
//     }
//
//     // Скрыть форму
//     hideForm() {
//       this.form.style.display = "none";
//     }
//
//     // Показать форму
//     viewForm() {
//       this.form.style.display = "flex";
//     }
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
//
// // Наследуемый класс
// export class SendForm extends Tst_BaseForm {
//   constructor(template, callback) {
//     // Вызываем конструктор родителя
//     super(template);
//
//     // Привязываем метод save к this
//     this.saveHandler = this.sendTask.bind(this);
//     // Привязываем метод cancel к this
//     this.cancelHandler = this.resetForm.bind(this);
//
//     this.callback = callback;
//
//   }
//
//   // Метод для настройки кнопки "Сохранить"
//   setupSaveButton() {
//     this.saveBtn.addEventListener("click", this.saveHandler);
//   }
//
//   // Метод для настройки кнопки "Отменить"
//   setupCancelButton() {
//     this.cancelBtn.addEventListener("click", this.cancelHandler);
//   }
//
//   // Метод для сброса формы
//   resetForm() {
//     this.clearFields();
//     this.hideForm();
//   }
//
//   // Формируем тело запроса для отправки на сервер
//   getRequestBody() {
//     return {
//       title: this.title.value,
//       description: this.description.value,
//       completed: false,
//       priority: this.priority,
//     };
//   }
//
//   // Обработка успешного ответа от сервера
//   handleResponse(data) {
//     console.log("Сервер вернул:", data);
//     // Можно вызвать resetForm() или другие действия
//     if (this.callback) {
//       this.callback(data);
//     }
//   }
//
//   // Обработка ошибок при отправке данных на сервер
//   handleError(error) {
//     console.error(error);
//     alert("Ошибка соединения с сервером");
//   }
//
//   async sendTask() {
//     const requestBody = this.getRequestBody();
//     try {
//       const response = await fetch("/tasks/create_task", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify(requestBody),
//         credentials: "include",
//       });
//       const data = await response.json();
//       this.handleResponse(data);
//     } catch (error) {
//       this.handleError(error);
//     }
//   }
// }
//
//
//
// // Наследуемый класс
// export class Tst_Task_Form extends Tst_BaseForm {
//   constructor(template, taskData) {
//     // Вызываем конструктор родителя
//     super(template);
//
//     this.data = taskData;
//
//   }
//
// }
