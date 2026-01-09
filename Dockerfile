ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /Vellory

#ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

#RUN chown -R appuser:appuser /Vellory

## Switch to the non-privileged user to run the application.
#USER appuser

## Копируем код и СРАЗУ меняем владельца на appuser
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

