import Form from "./Form.js";

export default class TaskManager {
  constructor(api, template, createTaskBtn, taskContainer) {
    // шаблон карточки
    this.template = template;
    // кнопка создания задачи
    this.createTaskBtn = createTaskBtn;
    // контейнер для задач
    this.taskContainer = taskContainer;
    // объект API
    this.api = api;

    // id карточки при создании Form
    this.formDatasetId = 0;
    //словарь для форм
    this.forms = new Map();

    // DOM-элемент карточки задачи, на который кликнули.
    this.selectedFormElement = null;
    // Объект Form карточки задачи, на который кликнули.
    this.selectedForm = null;

    // Обработчик кнопки создания задачи
    this.initCreateTaskHandler();
    // Обработчик клика по форме
    this.initTaskContainerHandler();
  }

  // Получить копию шаблона карточки
  getTemplateCopy() {
    return this.template.cloneNode(true);
  }

  // добавляет форму в словарь
  addToForms(form) {
    this.forms.set(form.datasetId, form);
    console.log("словарь обновлен", this.forms);
  }

  // Создает форму передавая копию шаблона карточки, родительский контейнер и id
  createForm() {
    const uniqueId = Date.now();
    const form = new Form(this.getTemplateCopy(), this.taskContainer, uniqueId);
    this.addToForms(form);
    return form;
  }

  getFormId() {
    return +this.selectedFormElement.dataset.id;
  }

  getForm() {
    const datasetId = this.getFormId();
    const form = this.forms.get(datasetId);
    if (!form) {
      return null;
    }
    return form;
  }

  removeForm() {
    const datasetId = this.getFormId();

    // Удаляем из Map
    this.forms.delete(datasetId);
    // Удаляем DOM-элемент
    this.selectedFormElement.remove();
    this.selectedFormElement = null;
  }

  // Обработчик клика
  initCreateTaskHandler() {
    if (!this.createTaskBtn) return;

    this.createTaskBtn.addEventListener("click", (event) => {
      event.preventDefault();
      const form = this.createForm();
      console.log("Форма создана", form);
    });
  }

  //Устанавливает временные атрибуты для удобного обращения к форме
  setTempAttributes(selectedForm) {
    this.selectedFormElement = selectedForm;
    this.selectedForm = this.getForm();
  }

  //Удаляет временные атрибуты
  clearTempAttributes() {
    this.selectedFormElement = null;
    this.selectedForm = null;
  }

  // Если создается впервые
  // Если уже была создана
  handleCancel() {
    if (this.selectedForm.created) {
      console.log("Задача уже создана");
    } else {
      try {
        this.removeForm();
        console.log("Форма удалена");
      } catch (error) {
        console.error("Failed to send task:", error);
      }
    }
  }

  async refreshFormData() {
    const form = this.selectedForm;
    //Собирает данные формы
    const data = form.getFormData();
    console.log("Данные из формы", data);

    let taskData;

    if (form.created) {
      taskData = await this.api.editTask(form.dbId, data);
      console.log("Данные с сервера после изменения", taskData);
    } else {
      //Отправляет данные формы на сервер, возвращает данные из БД
      taskData = await this.api.createTask(data);
      form.created = true;
      console.log("Данные с сервера после создания", taskData);
    }

    //Очищаем поля
    form.setFields();
    //Устанавливаем поля
    form.setFields(taskData);
    console.log(form);
    form.lockForm();
  }

  // Делегированный обработчик для taskContainer
  // Создаем обработчик на весь контейнер для задач
  initTaskContainerHandler() {
    this.taskContainer.addEventListener("click", async (event) => {
      const target = event.target; // Элемент, на который кликнули
      console.log(target);
      const selectedForm = target.closest(".task-container");
      if (!selectedForm) return; // Если клик был вне карточки — прекращаем обработку

      this.setTempAttributes(selectedForm); // Устанавливаем временные атрибуты.

      // const targetCircle = event.target.closest(".circle");
      //   if (targetCircle) {
      //
      //   }
      try {
        // Обработка кнокпи Отменить
        if (target.closest(".card-btn-cancel")) {
          this.handleCancel();
        }

        // Обработка кнокпи Сохарнить
        if (target.closest(".card-btn-save")) {
          await this.refreshFormData();
        }

        if (target.closest(".change-btn")) {
          this.selectedForm.unlockForm();
        }

        //Обработка клика по кругам выбора приоритета
        const targetCircle = target.closest(".circle");
        if (targetCircle) {
          const circleId = Number(targetCircle.dataset.id);
          console.log("id круга", circleId);
          this.selectedForm.setPriorityCircles(circleId);
        }
      } finally {
        this.clearTempAttributes(); // Обнуляем временные атрибуты.
      }
    });
  }
}
