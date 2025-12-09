export default class Form {
  constructor(template, container, datasetId, priority) {
    //Шаблон формы
    this.form = template;
    // Родительский контейнер для формы
    this.container = container;
    // id с фронта при создании
    this.datasetId = datasetId;
    //установка data-id атрибута
    this.form.dataset.id = datasetId;

    // Отобразить форму
    this.viewForm();

    // Поля формы
    this.title = this.form.querySelector(".card-title-input");
    this.description = this.form.querySelector(".card-content-input");
    this.formId = this.form.querySelector(".task-number");

    //id с Базы данных
    this.id = 0;
    this.priority = -1;
    console.log("this.priority", this.priority);
    this.circles = this.form.querySelectorAll(".circle");

    // true если задача создавалась
    this.created = false;
    // true если задача завершена
    this.completed = false;

    //Маска
    this.overlay = this.form.querySelector(".overlay");

    // Кнопки
    this.saveBtn = this.form.querySelector(".card-btn-save");
    this.cancelBtn = this.form.querySelector(".card-btn-cancel");
    this.changeBtn = this.form.querySelector(".change-btn");
    this.completeBtn = this.form.querySelector(".card-btn-complete");

    this.setPriorityCircles(priority);
  }

  completedTask() {
    this.completed = !this.completed;
    const tick = this.completeBtn.querySelector("#complete-tick");
    const circle = this.completeBtn.querySelector("#complete-circle");
    console.log("tick", tick);
    console.log("tick", circle);
    tick.classList.toggle("true");
    tick.classList.toggle("false");
    circle.classList.toggle("true");
    circle.classList.toggle("false");
    this.title.classList.toggle("text-completed");
    this.description.classList.toggle("text-completed");
    this.overlay.classList.toggle("active");
  }
  // Показать форму
  viewForm() {
    // Добавить элемент в контейнер
    this.container.appendChild(this.form);
    // Отобразить
    this.form.style.display = "flex";
  }

  getFormData() {
    return {
      title: this.title.value,
      description: this.description.value,
      priority: this.priority,
    };
  }

  setFields(data = {}) {
    this.title.value = data.title || ""; // если data.title нет — пустая строка
    this.description.value = data.description || "";
    this.priority = data.priority != null ? data.priority : -1;
    this.formId.textContent = data.id != null ? "#" + data.id : "";
    this.id = data.id != null ? data.id : 0;
  }

  // Переводим в режим просмотра, фиксацией элементов форме
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

  // Переводим форму в редактируемый режим
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

  // Принимает id круга по которому кликнули
  // Устанавливает приоритет задачи
  // Устанавливает цвет кругов
  setPriorityCircles(index) {
    // Устанавливаем приоритет
    // При повторном нажати на круг, сбрасываем приоритет.
    if (this.priority === index) {
      index = -1;
    }
    this.priority = index;

    // Перебираем круги, закрашиваем только <= index
    // Остальные transparent
    this.circles.forEach((c, i) => {
      // если индекс элемента <=
      if (i <= index) {
        c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
      } else {
        c.style.backgroundColor = "transparent"; // Сброс цвета
      }
    });
  }
}
