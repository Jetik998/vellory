export default class Form {
  constructor(template, container, datasetId, priority = 1) {
    // ===== Основные элементы =====
    this.form = template; // Шаблон формы
    this.container = container; // Родительский контейнер для формы
    this.datasetId = datasetId; // id с фронта при создании
    this.form.dataset.id = datasetId; // Установка data-id атрибута

    // ===== Поля формы =====
    this.title = this.form.querySelector(".card-title-input");
    this.description = this.form.querySelector(".card-content-input");
    this.formId = this.form.querySelector(".task-number");
    this.circles = this.form.querySelectorAll(".circle");

    // Маска для выполненной задачи
    this.overlay = this.form.querySelector(".overlay");

    // ===== Идентификаторы и приоритет =====
    this.id = 0; // id с бека
    this.priority = priority; // Приоритет задачи

    // ===== Состояния формы =====
    this.created = false; // true, если задача создавалась
    this.completed = false; // true, если задача завершена
    this.edit = false; // true, если задача редактируется

    // ===== Кнопки =====
    this.saveBtn = this.form.querySelector(".card-btn-save");
    this.cancelBtn = this.form.querySelector(".card-btn-cancel");
    this.changeBtn = this.form.querySelector(".change-btn");
    this.completeBtn = this.form.querySelector(".card-btn-complete");

    // ===== Инициализация =====
    // Обработка клика по кругу: устанавливаем приоритет и окрашиваем круги
    // this.setPriorityCircles(this.priority);

    // Показываем форму: добавляем в контейнер и делаем видимой
    this.viewForm();
  }

  updateCompletedAttribute() {
    this.completed = !this.completed;
  }

  updateCompletedState() {
    // path галочка внутри кнопки завершения
    const tick = this.completeBtn.querySelector("#complete-tick");
    // path круг внутри кнопки завершения
    const circle = this.completeBtn.querySelector("#complete-circle");

    // Активация/Деактивация кнопки Изменить
    this.changeBtn.disabled = this.completed;

    // Переключаем классы "true" и "false" для галочки и круга
    [tick, circle].forEach((el) => {
      el.classList.toggle("true", this.completed);
      el.classList.toggle("false", !this.completed);
    });

    // Переключаем класс "text-completed" для заголовка и описания задачи
    [this.title, this.description].forEach((el) => {
      el.classList.toggle("text-completed", this.completed);
    });

    // Скрыть/Показать маску для задачи
    this.overlay.classList.toggle("active", this.completed);
  }

  // Показать форму
  viewForm() {
    // Добавить элемент в контейнер
    this.container.appendChild(this.form);
    // Отобразить
    this.form.style.display = "flex";
  }

  // Возвращает данные формы: заголовок, описание и приоритет
  getFormData() {
    return {
      user_task_id: this.datasetId,
      title: this.title.value,
      priority: this.priority,
      description: this.description.value,
      completed: this.completed,
    };
  }

  // Заполняет поля формы данными из объекта data или сбрасывает их по умолчанию
  setFormData(data = {}) {
    this.created = true;
    this.completed = data.completed;
    this.priority = data.priority;
    this.id = data.id != null ? data.id : 0;
  }

  // Заполняет поля формы данными из объекта data или сбрасывает их по умолчанию
  setFields(data = {}) {
    this.title.value = data.title || ""; // если data.title нет — пустая строка
    this.description.value = data.description || "";
    this.formId.textContent =
      data.user_task_id != null ? "#" + data.user_task_id : "";
    this.setPriorityCircles(data.priority);
    this.updateCompletedState();
  }

  // Блокирует форму: делает поля и круги некликабельными, показывает/скрывает кнопки
  lockForm() {
    // Отключаем поля ввода
    [this.title, this.description].forEach((el) => (el.disabled = true));

    // Делаем круги приоритетов некликабельными
    this.circles.forEach((c) => (c.style.pointerEvents = "none"));

    // Скрываем кнопки сохранения и отмены
    this.saveBtn.style.display = "none";
    this.cancelBtn.style.display = "none";
    this.changeBtn.style.display = "flex";
    this.completeBtn.style.display = "flex";
  }

  // Разблокирует форму
  unlockForm() {
    // Включаем поля ввода
    [this.title, this.description].forEach((el) => (el.disabled = false));

    // Делаем круги приоритетов кликабельными
    this.circles.forEach((c) => (c.style.pointerEvents = "auto"));

    // Показываем кнопки сохранения и отмены
    this.saveBtn.style.display = "flex";
    this.cancelBtn.style.display = "flex";

    // Скрываем кнопки изменения и завершения
    this.changeBtn.style.display = "none";
    this.completeBtn.style.display = "none";
  }

  // Устанавливает приоритет задачи и окрашивает круги до выбранного
  // Если кликнули на уже выбранный круг, приоритет сбрасывается
  setPriorityCircles(index) {
    // Устанавливаем приоритет
    // При повторном нажати на круг, сбрасываем приоритет.
    if (this.priority === index) {
      index = 1;
    }
    this.priority = index;

    // Перебираем круги, закрашиваем только <= index
    // Остальные transparent
    this.circles.forEach((c, i) => {
      // если индекс элемента <=
      if (i <= index - 2) {
        c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
      } else {
        c.style.backgroundColor = "transparent"; // Сброс цвета
      }
    });
  }
}
