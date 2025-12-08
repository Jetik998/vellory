// import Form from "./Form_copy.js";
//
// export default class TaskManager {
//   constructor(template, createTaskBtn, taskContainer) {
//     this.template = template;
//     this.createTaskBtn = createTaskBtn;
//     this.taskContainer = taskContainer;
//
//     this.frontId = 0;
//     this.forms = new Map();
//
//     this.initCreateTaskHandler();
//     this.initTaskContainerHandler();
//   }
//
//   // Получить копию шаблона карточки
//   formCopy() {
//     return this.template.cloneNode(true);
//   }
//
//   // Создать форму
//   createTaskForm() {
//     this.frontId += 1;
//     return new Form(this.formCopy(), this.taskContainer, this.frontId);
//   }
//
//   addForm(form) {
//     this.forms.set(form.id, form);
//   }
//
//
//   // Обработчик клика
//   initCreateTaskHandler() {
//     if (!this.createTaskBtn) return;
//
//     this.createTaskBtn.addEventListener("click", (event) => {
//       event.preventDefault();
//       const form = this.createTaskForm();
//       this.addForm(form);
//     });
//   }
//   getForm(card) {
//       const frontId = Number(card.dataset.id);
//       console.log(frontId);
//       console.log(this.forms);
//       return this.forms.get(frontId) ?? null; // вернет null если не найдено
//   }
//
//       // Делегированный обработчик для taskContainer
//   // Навешиваем делегированный обработчик на весь контейнер карточек
//   initTaskContainerHandler() {
//
//     this.taskContainer.addEventListener("click", async (event) => {
//       console.log("click");
//       const target = event.target; // Элемент, на который кликнули
//       console.log(target);
//       const card = target.closest(".task-container");  // Находим карточку с задачей.
//       console.log(card);
//       if (!card) return;// Если клик был вне карточки — прекращаем обработку
//
//       // const targetCircle = event.target.closest(".circle");
//       //   if (targetCircle) {
//       //
//       //   }
//
//       const cancelBtn = target.closest(".card-btn-cancel");
//       console.log(cancelBtn);
//       if (cancelBtn) {
//         const form = this.getForm(card);
//         console.log(form);
//         if (!form) return; // Если объект не найден — выходим
//         try {
//           const result = await form.resetForm();
//           console.log("Task sent:", result);
//         } catch (error) {
//           console.error("Failed to send task:", error);
//         }
//       }
//     });
//   }
//
// }
