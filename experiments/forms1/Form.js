// export default class Form {
//   constructor(template, container, id) {
//     this.form = template;
//     // Контейнер для формы
//     this.container = container;
//     // id с фронта
//     this.id = id;
//     //dataset id для фронта
//     this.form.dataset.id = id;
//
//     // Отобразить форму
//     this.viewForm();
//
//     // Данные формы
//     this.title = this.form.querySelector(".card-title-input");
//     this.description = this.form.querySelector(".card-content-input");
//     this.formId = this.form.querySelector(".task-number");
//     this.intId = 0;
//     this.priority = 0;
//     this.circles = this.form.querySelectorAll(".circle");
//
//     // true если задача создавалась
//     this.taskCreated = false;
//
//     // // Кнопки
//     // this.saveBtn = this.form.querySelector(".card-btn-save");
//     // this.cancelBtn = this.form.querySelector(".card-btn-cancel");
//     // this.changeBtn = this.form.querySelector(".change-btn");
//     // // Привязываем метод sendTask
//     // this.saveHandler = this.sendTask.bind(this);
//     // // Привязываем метод resetForm
//     // this.cancelHandler = this.resetForm.bind(this);
//     // // Привязываем метод
//     // this.changeHandler = this.unlockForm.bind(this);
//     // // Назначаем обработчики
//     // this.setupSaveButton();
//     // this.setupCancelButton();
//     // this.setupChangeButton();
//
//     // Настройка кругов приоритета
//     this.setupPriorityCircles();
//   }
//   // // Настройка кнопки "Сохранить"
//   // setupSaveButton() {
//   //   this.saveBtn.addEventListener("click", this.saveHandler);
//   // }
//   //
//   // // Настройка кнопки "Отменить"
//   // setupCancelButton() {
//   //   this.cancelBtn.addEventListener("click", this.cancelHandler);
//   // }
//   //
//   // // Настройка кнопки "Изменить"
//   // setupChangeButton() {
//   //   this.changeBtn.addEventListener("click", this.changeHandler);
//   // }
//
//   // Обновление данных формы
//   setFields(data = {}) {
//     this.title.value = data.title || ""; // если data.title нет — пустая строка
//     this.description.value = data.description || "";
//     this.priority = data.priority !== undefined ? data.priority : 0; // 0 по умолчанию
//     this.setPriorityCircles(this.priority);
//     this.formId.textContent = "#" + data.id || "";
//     this.intId = data.id; // Сохраняем ID задачи
//   }
//
//   // // Удаление обработчиков кнопок
//   // removeButtonHandlers() {
//   //   if (this.saveBtn && this.saveHandler) {
//   //     this.saveBtn.removeEventListener("click", this.saveHandler);
//   //   }
//   //   if (this.cancelBtn && this.cancelHandler) {
//   //     this.cancelBtn.removeEventListener("click", this.cancelHandler);
//   //   }
//   // }
//
//   // Скрыть форму
//   hideForm() {
//     this.form.style.display = "none";
//   }
//
//   resetForm() {
//     this.setFields();
//     this.hideForm();
//     // this.removeButtonHandlers();
//   }
//
//   // Показать форму
//   viewForm() {
//     // Добавить элемент в контейнер
//     this.container.appendChild(this.form);
//     // Отобразить
//     this.form.style.display = "flex";
//   }
//
//   // Обработка ошибок при отправке данных на сервер
//   handleError(error) {
//     console.error(error);
//     alert("Ошибка соединения с сервером");
//   }
//
//   // Обработка успешного ответа от сервера
//   handleResponse(data) {
//     console.log("Сервер вернул:", data);
//   }
//
//   // Формируем тело запроса для отправки на сервер
//   getRequestBody(
//     fields = ["id", "title", "description", "completed", "priority"],
//   ) {
//     const fullBody = {
//       id: this.intId,
//       title: this.title.value,
//       description: this.description.value,
//       completed: false,
//       priority: this.priority,
//     };
//
//     // Создаем новый объект с только нужными полями
//     const filteredBody = {};
//     fields.forEach((key) => {
//       if (key in fullBody) {
//         filteredBody[key] = fullBody[key];
//       }
//     });
//
//     console.log(filteredBody);
//     return filteredBody;
//   }
//
//   // Переводим в режим просмотра, фиксацией элементов форме
//   lockForm() {
//     // Отключаем поля ввода
//     [this.title, this.description].forEach((el) => (el.disabled = true));
//
//     // Делаем круги приоритетов некликабельными
//     this.circles.forEach((c) => (c.style.pointerEvents = "none"));
//
//     // Скрываем кнопки сохранения и отмены
//     if (this.saveBtn) this.saveBtn.style.display = "none";
//     if (this.cancelBtn) this.cancelBtn.style.display = "none";
//     if (this.changeBtn) this.changeBtn.style.display = "flex";
//   }
//
//   // Переводим форму в редактируемый режим
//   unlockForm() {
//     // Включаем поля ввода
//     [this.title, this.description].forEach((el) => (el.disabled = false));
//
//     // Делаем круги приоритетов кликабельными
//     this.circles.forEach((c) => (c.style.pointerEvents = "auto"));
//
//     // Показываем кнопки сохранения и отмены
//     if (this.saveBtn) this.saveBtn.style.display = "flex";
//     if (this.cancelBtn) this.cancelBtn.style.display = "flex";
//
//     // Скрываем кнопку изменения
//     if (this.changeBtn) this.changeBtn.style.display = "none";
//   }
//
//   // Новый метод для обработки ответа
//   async handleFetchResponse(response, successMessage) {
//     const data = await response.json(); // получаем тело ответа
//     if (response.ok) {
//       this.handleResponse(data); // обрабатываем успешный ответ
//       this.setFields(data); // обновляем форму
//       this.lockForm(); // блокируем форму после обновления
//       console.log(successMessage);
//     } else {
//       console.error("Ошибка при выполнении запроса:", data);
//     }
//   }
//
//   async changeTask() {
//     const requestBody = this.getRequestBody([
//       "title",
//       "description",
//       "completed",
//       "priority",
//     ]);
//     try {
//       console.log("changeTask", requestBody.priority);
//       const response = await fetch("/tasks/" + this.intId, {
//         method: "PATCH",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(requestBody),
//         credentials: "include",
//       });
//
//       await this.handleFetchResponse(response, "Задача успешно обновлена!");
//     } catch (error) {
//       this.handleError(error); // обработка сетевых ошибок
//     }
//   }
//
//   async createTask() {
//     const requestBody = this.getRequestBody([
//       "title",
//       "description",
//       "completed",
//       "priority",
//     ]);
//     try {
//       const response = await fetch("/tasks/create_task", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(requestBody),
//         credentials: "include",
//       });
//
//       await this.handleFetchResponse(response, "Задача успешно создана!");
//     } catch (error) {
//       this.handleError(error); // обработка сетевых ошибок
//     }
//   }
//
//   async sendTask() {
//     if (this.taskCreated) {
//       // Задача уже создана — обновляем её
//       await this.changeTask();
//     } else {
//       // Задача ещё не создана — создаём новую
//       await this.createTask();
//       // После успешного создания можно отметить, что задача теперь создана
//       this.taskCreated = true;
//     }
//   }
//
//   // Метод для настройки кликов по кругам приоритетов
//   setupPriorityCircles() {
//     // Ищет внутри карточки задачи все элементы с классом .circle.
//     const circles = this.circles;
//     // Проходим по каждому кругу и назначаем обработчик клика.
//     circles.forEach((circle, index) => {
//       // Создаём функцию, которая при клике будет вызывать метод togglePriority и передавать: все круги (circles), индекс текущего круга (index)
//       const handler = () => this.activatePriorityCircles(circles, index);
//
//       // Привязываем обработчик клика к кругу.
//       circle.addEventListener("click", handler);
//     });
//   }
//
//   setPriorityCircles(index) {
//     // Сдвигаем индекс на 1, если нужно выравнивание
//     index = index - 1;
//     this.circles.forEach((c, i) => {
//       if (i <= index) {
//         c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
//       } else {
//         c.style.backgroundColor = "transparent"; // Сброс цвета
//       }
//     });
//   }
//
//   // Метод для изменения приоритета задачи при клике на круг
//   activatePriorityCircles(circles, index) {
//     // Сохраняем выбранный приоритет
//     this.priority = index + 1;
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
//       // Если
//       if (isActive) {
//         this.priority = 0;
//       }
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
