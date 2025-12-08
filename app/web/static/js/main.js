import { setupUser } from "./userService.js";
import { setupAvatar } from "./avatars.js";
import { setupLogout } from "./logout.js";
import TaskManager from "./TaskManager.js";
import Api from "./Api.js";

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.getElementById("logoutButton");
  const userAvatar = document.getElementById("user-avatar-img");
  const fileInput = document.getElementById("fileInput");
  const usernameCaption = document.getElementById("username-caption");
  const changeAvatar = document.getElementById("ChangeAvatar");
  const taskTemplate = document.querySelector(".task-container");
  const createTaskBtn = document.getElementById("create-task");
  const taskContainer = document.querySelector(".person-boxes");

  const api = new Api();

  window.taskManager = new TaskManager(
    api,
    taskTemplate,
    createTaskBtn,
    taskContainer,
  );

  // Получить пользователя
  await setupUser(userAvatar, usernameCaption);

  setupAvatar(userAvatar, changeAvatar, fileInput);

  setupLogout(logoutButton);
});
