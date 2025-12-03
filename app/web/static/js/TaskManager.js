import Form from "./Form.js";

export default class TaskManager {
  constructor(template, createTaskBtn, taskContainer) {
    this.template = template;
    this.createTaskBtn = createTaskBtn;
    this.taskContainer = taskContainer;

    this.initCreateTaskHandler();
  }

  // Получить копию шаблона карточки
  formCopy() {
    return this.template.cloneNode(true);
  }

  // Создать форму
  createTaskForm() {
    const form = new Form(this.formCopy(), this.taskContainer);
  }

  // Обработчик клика
  initCreateTaskHandler() {
    if (!this.createTaskBtn) return;

    this.createTaskBtn.addEventListener("click", (event) => {
      event.preventDefault();
      this.createTaskForm();
    });
  }
}
