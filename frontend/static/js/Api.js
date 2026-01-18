export default class Api {
  constructor() {
    this.taskUrl = "/tasks";
    this.userUrl = "/users";
    this.refreshPromise = null;
  }

  handleError(error) {
    console.error(error);
  }

  async fetchWithRefresh(url, options = {}, isRetry = false) {
    let response = await fetch(url, { ...options, credentials: "include" });

    if (response.status === 401 && !isRetry) {
      if (this.refreshPromise) {
        await this.refreshPromise;
      } else {
        this.refreshPromise = this.refreshToken().finally(() => {
          this.refreshPromise = null;
        });
        await this.refreshPromise;
      }

      // Повторяем только один раз с флагом isRetry = true
      response = await this.fetchWithRefresh(url, options, true);
    }

    return response;
  }

  async refreshToken() {
    console.log("DEBUG: Рефреш токена...");

    try {
      const refreshResponse = await fetch("/auth/refresh", {
        method: "POST",
        credentials: "include",
      });

      if (!refreshResponse.ok) {
        console.log("DEBUG: Рефреш не удался");
        window.location.href = "/login";
        throw new Error("Refresh failed");
      }

      console.log("DEBUG: Рефреш успешен");
      return refreshResponse;
    } catch (error) {
      window.location.href = "/login";
      throw error;
    }
  }

  // Универсальный метод для всех запросов
  async request(url, options = {}) {
    try {
      const response = await this.fetchWithRefresh(url, options);
      const data = await response.json();

      if (response.ok) {
        return data;
      } else {
        console.error("Ошибка при выполнении запроса:", data);
        return null;
      }
    } catch (error) {
      this.handleError(error);
      return null;
    }
  }

  async getAllTasks(filters = {}) {
    const params = new URLSearchParams();
    params.append("completed", String(false));
    params.append("order_by_created", String(true));

    return this.request(`${this.taskUrl}/?${params.toString()}`, {
      method: "GET",
    });
  }

  async createTask(data) {
    return this.request(`${this.taskUrl}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  }

  async editTask(id, data) {
    return this.request(`${this.taskUrl}/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  }

  async deleteTask(id) {
    return this.request(`${this.taskUrl}/${id}`, {
      method: "DELETE",
    });
  }

  async uploadAvatar(formData) {
    return this.request(`${this.userUrl}/avatar/upload`, {
      method: "POST",
      body: formData,
    });
  }
}
