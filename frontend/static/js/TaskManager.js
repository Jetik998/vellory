import Form from "./Form.js";

export default class TaskManager {
  constructor(api, template, createTaskBtn, taskContainer) {
    // ===== Элементы интерфейса =====
    this.template = template; // Шаблон карточки
    this.createTaskBtn = createTaskBtn; // Кнопка создания задачи
    this.taskContainer = taskContainer; // Контейнер для задач

    // ===== Флаг состояния создания новой задачи =====
    this.isCreatingTask = false;

    // ===== API =====
    this.api = api; // Объект API для работы с сервером
    this.lastTaskId = 1;

    // ===== Формы =====
    this.forms = new Map(); // Словарь для хранения форм

    // ===== Выбранная карточка =====
    this.selectedFormElement = null; // DOM-элемент карточки, на который кликнули
    this.selectedForm = null; // Объект Form карточки, на который кликнули

    // ===== Инициализация обработчиков =====
    this.initCreateTaskHandler(); // Обработчик кнопки создания задачи
    this.initTaskContainerHandler(); // Обработчик клика по контейнеру с задачами
  }

  // Возвращает копию шаблона карточки для создания новой задачи
  getTemplateCopy() {
    return this.template.cloneNode(true);
  }

  // Добавляет форму в словарь forms по её datasetId
  addToForms(form) {
    this.forms.set(form.datasetId, form);
  }

  // Создает новую форму для задачи, добавляет её в словарь и возвращает объект Form
  createForm() {
    // Флаг состояния создания задачи
    const form = new Form(
      this.getTemplateCopy(),
      this.taskContainer,
      this.lastTaskId,
    );

    this.addToForms(form);

    return form;
  }

  refreshData(form, taskData) {
    form.setFormData(taskData); // Заполнение Form данными с сервера
    form.setFields(); // Очистка полей
    form.setFields(taskData); // Заполнение полей данными с сервера
    // 5. Блокируем форму для редактирования
    form.lockForm();
  }

  // Загружает задачи с сервера, создает формы, заполняет их данными, блокирует и помечает как созданные
  async initTasks() {
    try {
      const tasks = await this.api.getAllTasks(); // 1. API возвращает массив задач

      tasks.forEach((taskData) => {
        const form = this.createForm();
        this.refreshData(form, taskData);
        this.lastTaskId++;
      });
    } catch (error) {
      console.error("Ошибка при загрузке задач с сервера:", error);
    }
  }

  // Обновляет данные формы: создаёт новую или редактирует существующую, затем блокирует форму
  async refreshFormData() {
    const form = this.selectedForm;
    if (!form) return;

    // 1. Собираем данные из формы
    const data = form.getFormData();

    let taskData;

    if (form.created) {
      // 2. Если форма уже создана, обновляем данные на сервере
      taskData = await this.api.editTask(form.id, data);
    } else {
      // 3. Если форма новая, создаём её на сервере
      taskData = await this.api.createTask(data);
      this.lastTaskId++;
    }
    this.refreshData(form, taskData);
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
    try {
      const datasetId = this.getFormId();
      // Удаляем из Map
      this.forms.delete(datasetId);
      // Удаляем из Map
      this.selectedFormElement.remove();
      this.selectedFormElement = null;
    } catch (error) {
      console.error("Failed to remove form:", error);
    }
  }

  // Обработчик клика по кнопке создания задачи
  initCreateTaskHandler() {
    if (!this.createTaskBtn) return;

    this.createTaskBtn.addEventListener("click", (event) => {
      if (!this.isCreatingTask) {
        this.isCreatingTask = true;
        event.preventDefault();
        this.createForm();
      }
    });
  }

  // Устанавливает временные ссылки на выбранную форму и её объект для удобного доступа
  setTempAttributes(selectedForm) {
    this.selectedFormElement = selectedForm;
    this.selectedForm = this.getForm();
  }

  // Очищает временные ссылки на выбранную форму
  clearTempAttributes() {
    this.selectedFormElement = null;
    this.selectedForm = null;
  }

  // Обрабатывает отмену редактирования или удаления формы
  async handleCancel() {
    const form = this.selectedForm;
    if (!form) return;

    // Если форма уже была создана, удаляем её с сервера
    if (form.created) {
      const data = await this.api.deleteTask(form.id);
      if (!data.success) {
        return;
      }
    }

    // Удаляем форму
    this.removeForm();
    this.isCreatingTask = false;
  }

  // // Добавляет обработчик кликов по задачам и выполняет действия в зависимости от нажатой кнопки
  initTaskContainerHandler() {
    this.taskContainer.addEventListener("click", async (event) => {
      const target = event.target; // Элемент, на который кликнули

      const selectedForm = target.closest(".task-container");
      if (!selectedForm) return; // Если клик был вне карточки — прекращаем обработку

      this.setTempAttributes(selectedForm); // Устанавливаем временные ссылки на выбранную форму

      try {
        // 1. Обработка кнопки "Отменить"
        if (target.closest(".card-btn-cancel")) {
          await this.handleCancel();
          this.isCreatingTask = false;
        }

        // 2. Обработка кнопки "Сохранить"
        if (target.closest(".card-btn-save")) {
          await this.refreshFormData();
          this.isCreatingTask = false;
        }

        // 3. Обработка кнопки "Изменить"
        if (target.closest(".change-btn")) {
          this.selectedForm.unlockForm();
        }

        // 4. Обработка кнопки "Выполнить"
        if (target.closest(".card-btn-complete")) {
          this.selectedForm.updateCompletedAttribute();
          await this.refreshFormData();
          this.isCreatingTask = false;
        }

        // 5. Обработка клика по элементам выбора приоритета
        const targetCircle = target.closest(".circle");
        if (targetCircle) {
          const circleId = Number(targetCircle.dataset.id);
          this.selectedForm.setPriorityCircles(circleId + 2);
        }
      } finally {
        // 6. Сбрасываем временные атрибуты после обработки
        this.clearTempAttributes();
      }
    });
  }
}
