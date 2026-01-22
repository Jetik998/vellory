ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем зависимости в отдельную папку
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- ЭТАП 2: Финальный образ (Runner) ---
FROM python:${PYTHON_VERSION}-slim AS runner

WORKDIR /Vellory

# Копируем ТОЛЬКО установленные зависимости
COPY --from=builder /install /usr/local

## Копируем код и СРАЗУ меняем владельца на appuser
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

