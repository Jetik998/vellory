import { setupUser } from "./userService.js";
import { setupCreateTask } from "./taskService.js";
import { setupAvatar } from "./avatars.js";
import { setupLogout } from "./logout.js";
import BaseForm from "./BaseForm.js";

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.getElementById("logoutButton");
  const userAvatar = document.getElementById("user-avatar-img");
  const fileInput = document.getElementById("fileInput");
  const usernameCaption = document.getElementById("username-caption");
  const changeAvatar = document.getElementById("ChangeAvatar");
  const createTaskBtn = document.getElementById("create-task");

  const taskTemplate = document.querySelector(".task-container");

  // Базовая форма для создания задачи
  const taskForm = new BaseForm(taskTemplate);

  const taskManager = new TaskManager();
  // Получить пользователя
  await setupUser(userAvatar, usernameCaption);

  // Обработчик для кнопки создания задач
  setupCreateTask(createTaskBtn, taskForm);

  setupAvatar(userAvatar, changeAvatar, fileInput);

  setupLogout(logoutButton);
});
