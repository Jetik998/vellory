import { setupUser } from "./userService.js";
import { setupCreateTask } from "./taskService.js";
import { setupAvatar } from "./avatars.js";
import { setupLogout } from "./logout.js";

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.getElementById("logoutButton");
  const userAvatar = document.getElementById("user-avatar-img");
  const fileInput = document.getElementById("fileInput");
  const usernameCaption = document.getElementById("username-caption");
  const changeAvatar = document.getElementById("ChangeAvatar");
  const createTaskBtn = document.getElementById("create-task");

  const taskTemplate = document.querySelector(".task-container");
  const taskContainer = document.querySelector(".person-boxes");

  // Получить пользователя

  await setupUser(userAvatar, usernameCaption);
  setupCreateTask(createTaskBtn, taskTemplate, taskContainer);
  setupAvatar(userAvatar, changeAvatar, fileInput);
  setupLogout(logoutButton);
});
