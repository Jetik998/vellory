export default class BaseForm {
  constructor(template) {
    this.form = template;
    this.title = this.form.querySelector(".card-title-input");
    this.description = this.form.querySelector(".card-content-input");
    this.priority = 0;
    this.saveBtn = this.form.querySelector(".card-btn-save");
    this.cancelBtn = this.form.querySelector(".card-btn-cancel");

    this.setupPriorityCircles();
  }

  // Метод для настройки кликов по кругам приоритетов
  setupPriorityCircles() {
    // Ищет внутри карточки задачи все элементы с классом .circle.
    const circles = this.form.querySelectorAll(".circle");
    // Проходим по каждому кругу и назначаем обработчик клика.
    circles.forEach((circle, index) => {
      // Создаём функцию, которая при клике будет вызывать метод togglePriority и передавать: все круги (circles), индекс текущего круга (index)
      const handler = () => this.activatePriorityCircles(circles, index);

      // Сохраняем выбранный приоритет
      this.priority = index;
      // Привязываем обработчик клика к кругу.
      circle.addEventListener("click", handler);
    });
  }

  // Метод для изменения приоритета задачи при клике на круг
  activatePriorityCircles(circles, index) {
    // Выбранный круг, на который кликнули.
    const circle = circles[index];
    // Флаг нажат ли круг. 1 нажатие true второе false
    const isActive = circle.classList.contains("active");
    // c - текущий круг i - его индекс circles - все круги
    // Если круг был нажат / isActive = true, делаем все круги прозрачными
    // Иначе / isActive = false, в цикле для всех кругов до нажатого включительно, устанавливаем цвет.
    // !Сбрасываем флаг active у всех, тк если флаг 2 = true то при нажатии флага 3
    // информация о состоянии флага 2 уже не нужна.
    circles.forEach((c, i) => {
      if (!isActive && i <= index) {
        c.classList.remove("active"); // Сбрасываем флаг у всех
        c.style.backgroundColor = c.dataset.color; // Устанавливаем цвет из data-атрибута
        circle.classList.add("active"); // Активируем выбранный круг
      } else {
        c.classList.remove("active"); // Деактивируем все остальные
        c.style.backgroundColor = "transparent"; // Сброс цвета
      }
    });
  }
}
