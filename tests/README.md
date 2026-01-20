# Тесты проекта

## Как запускать

Все тесты:
pytest

Один файл:
pytest unit/test_api.py -v -s

Только schemathesis:
pytest -k schemathesis -v

---

## Полезные флаги

-v — подробные имена тестов  
-s — показывать print и логи  
-x — остановиться на первой ошибке

---

## Schemathesis

Берёт OpenAPI прямо из FastAPI:
schema = schemathesis.openapi.from_asgi("/openapi.json", app=app)

Если падает — проверить endpoint или operation_id.
