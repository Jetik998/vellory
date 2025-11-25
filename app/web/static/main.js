import * as userService from "./userService.js";
import { setupCreateTaskButton } from "./taskService";
import { setupAvatar } from "./avatars.js";
import { setupLogout } from "./logout.js";

document.addEventListener("DOMContentLoaded", async () => {
  const logoutButton = document.getElementById("logoutButton");
  const userAvatar = document.getElementById("user-avatar-img");
  const fileInput = document.getElementById("fileInput");
  const usernameCaption = document.getElementById("username-caption");
  const changeAvatar = document.getElementById("ChangeAvatar");
  const createTaskBtn = document.getElementById("create-task");

  const user = await userService.getUser();
  await userService.updateUserData(user, userAvatar, usernameCaption);
  setupCreateTaskButton(createTaskBtn);
  setupAvatar(userAvatar, changeAvatar, fileInput);
  setupLogout(logoutButton);
});
