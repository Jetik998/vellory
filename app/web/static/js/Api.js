export default class Api {
  constructor() {
    //Шаблон формы
    this.baseUrl = "/tasks";
  }

  // Обработка ошибок при отправке данных на сервер
  handleError(error) {
    console.error(error);
    alert("Ошибка соединения с сервером");
  }

  // Обработка ответа
  async handleFetchResponse(response, successMessage) {
    const data = await response.json(); // получаем тело ответа
    if (response.ok) {
      console.log(successMessage);
      return data;
    } else {
      console.error("Ошибка при выполнении запроса:", data);
    }
  }

  //Создать задачу
  async createTask(data) {
    try {
      const response = await fetch(this.baseUrl + "/create_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
      });
      return await this.handleFetchResponse(
        response,
        "Задача успешно создана!",
      );
    } catch (error) {
      this.handleError(error); // обработка сетевых ошибок
    }
  }

  //Создать задачу
  async editTask(id, data) {
    try {
      const response = await fetch(`${this.baseUrl}/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
      });
      return await this.handleFetchResponse(
        response,
        "Задача успешно изменена!",
      );
    } catch (error) {
      this.handleError(error); // обработка сетевых ошибок
    }
  }
}
