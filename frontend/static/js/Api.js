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
      return data;
    } else {
      console.error("Ошибка при выполнении запроса:", data);
    }
  }

  async getAllTasks(filters = {}) {
    const params = new URLSearchParams();

    // Добавляем параметры
    params.append("completed", String(false));
    params.append("order_by_created", String(true));

    //Формируем путь
    const url = this.baseUrl + "/?" + params.toString();
    try {
      const response = await fetch(url, {
        method: "GET",
        credentials: "include",
      });

      return await this.handleFetchResponse(
        response,
        "Задачи успешно получены!",
      );
    } catch (error) {
      this.handleError(error);
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

  //Удалить
  async deleteTask(id) {
    try {
      const response = await fetch(`${this.baseUrl}/${id}`, {
        method: "DELETE",
        credentials: "include",
      });
      return await this.handleFetchResponse(
        response,
        "Задача успешно удалена!",
      );
    } catch (error) {
      this.handleError(error); // обработка сетевых ошибок
    }
  }
}
