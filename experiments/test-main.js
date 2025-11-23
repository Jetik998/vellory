// const circles = document.querySelectorAll(".circle");
// let taskPriority = 0;
//
// circles.forEach((circle, index) => {
//   circle.addEventListener("click", () => {
//     // Проверяем, активен ли последний кликнутый круг
//     const isActive = circle.classList.contains("active");
//
//     circles.forEach((c, i) => {
//       if (!isActive && i <= index) {
//         c.classList.remove("active");
//         c.style.backgroundColor = c.dataset.color;
//         circle.classList.add("active");
//       } else {
//         c.classList.remove("active");
//         c.style.backgroundColor = "transparent";
//       }
//     });
//     taskPriority = isActive ? 0 : index + 1;
//   });
// });

// // Функция для сброса всех кружков в прозрачные
// function resetCircles() {
//   circles.forEach((circle) => {
//     circle.style.backgroundColor = "transparent";
//   });
//   taskPriority = 0; // сброс приоритета
// }
