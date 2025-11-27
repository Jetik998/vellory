// async function sendRouteRequest(url) {
//   try {
//     const res = await fetch(url, { method: "GET" });
//
//     if (res.ok) {
//       return true;
//     } else {
//       const errText = await res.text();
//       console.error("Server error:", errText);
//       return false;
//     }
//   } catch (e) {
//     console.error("Network error:", e);
//     return false;
//   }
// }
//
// // Пытаемся постучатся на / если ок получаем index.html
// // если не получается пытаемся на /refresh есл ок получаем токены и пробуем снова на /
// // если все False остаемся на /login
//
// async function attemptSiteAccess() {
//   const step2 = await sendRouteRequest("/refresh");
//
//   if (step2) {
//     window.location.href = "/";
//   }
// }
//
// attemptSiteAccess().catch(console.error);
