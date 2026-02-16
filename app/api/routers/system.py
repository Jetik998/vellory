import os
import sys
import psutil
import fastapi
from fastapi import APIRouter, Response
from datetime import datetime, timezone
import time

from starlette.responses import JSONResponse

from app.api.dependencies import rate_limiter
from app.enums import Tags
from app.middleware import response_times, request_count
from app.api.utils import format_uptime, check_dependencies

router = APIRouter(prefix="/system", tags=[Tags.system])

APP_VERSION = fastapi.__version__
start_time = time.time()


@router.get(
    "/health", dependencies=[rate_limiter], summary="Проверка доступности сервиса"
)
async def health():
    """
    **Быстрая проверка работоспособности**
    """
    return Response(status_code=200)


# Version
@router.get(
    "/version", dependencies=[rate_limiter], summary="Информация о версии приложения"
)
async def version():
    """
    **Информация о текущей версии приложения и среде выполнения**

    ---

    - Возвращает основные данные о версии сервиса, дате сборки и среде выполнения.
    - Полезно для мониторинга, отладки и проверки совместимости клиентов с API.
    - Поля ответа:
        - **version** — текущая версия приложения
        - **build_date** — дата сборки приложения
        - **python_version** — версия Python, на которой работает сервис
        - **api_version** — версия API
    """
    return {
        "version": APP_VERSION,
        "build_date": "2025-09-01",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "api_version": "v1",
    }


@router.get(
    "/metrics", dependencies=[rate_limiter], summary="Метрики производительности"
)
async def metrics():
    """
    **Метрики производительности сервиса**

    ---

    - Возвращает основные метрики работы сервиса.
    - Метрики включают:
        - Время работы сервиса (секунды) (**uptime_seconds**) и форматированное (**uptime_formatted**)
        - Количество обработанных запросов (**request_count**)
        - Среднее время ответа сервиса в миллисекундах (**average_response_time_ms**)
        - Использование памяти процесса: RSS в мегабайтах (**rss_mb**) и процент (**percent**)
        - Загрузка CPU процесса (**cpu_percent**)
        - Временная метка генерации метрик (UTC) (**timestamp**)
    - Полезно для мониторинга состояния сервиса и анализа производительности.
    """
    uptime = time.time() - start_time

    # Расчет среднего времени ответа
    avg_response_time = (
        sum(response_times) / len(response_times) if response_times else 0
    )

    # Информация о памяти
    process = psutil.Process()
    memory_info = process.memory_info()

    return {
        "uptime_seconds": round(uptime, 2),
        "uptime_formatted": format_uptime(uptime),
        "request_count": request_count,
        "average_response_time_ms": round(avg_response_time * 1000, 2),
        "memory": {
            "rss_mb": round(memory_info.rss / 1024 / 1024, 2),
            "percent": round(process.memory_percent(), 2),
        },
        "cpu_percent": round(process.cpu_percent(interval=0.1), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/status")
async def status():
    """
    **Статус сервиса и состояние зависимостей**

    ---

    - Возвращает расширенную информацию о текущем статусе сервиса и его зависимостях.
    - Полезно для мониторинга работоспособности сервиса и проверки состояния внешних компонентов.
    - Поля ответа:
        - Название сервиса (**service**)
        - Статус работы сервиса (**status**)
        - Время работы сервиса в секундах (**uptime_seconds**)
        - Статус зависимостей (**dependencies**) — результат проверки внешних сервисов/ресурсов
        - Среда выполнения (**environment**)
        - Временная метка генерации статуса (UTC) (**timestamp**)
    - Пример использования: интеграция с системами мониторинга, автоматическое оповещение о недоступности зависимостей.
    """
    uptime = time.time() - start_time

    # Здесь можно добавить проверки реальных зависимостей
    dependencies_status = await check_dependencies()

    return {
        "service": "Vellory",
        "status": "running",
        "uptime_seconds": round(uptime, 2),
        "dependencies": dependencies_status,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/debug")
async def debug():
    """
    **Отладочная информация о сервисе и системе (только для разработки)**

    ---

    - Возвращает детальную информацию о текущем состоянии сервиса, процессах и системе.
    - Доступен только в средах, отличных от production. В продакшене возвращает ошибку 403.
    - Полезно для локальной разработки, отладки и мониторинга метрик сервиса.
    - Поля ответа:
        - **environment** — информация о среде выполнения:
            - версия Python (**python_version**)
            - платформа (**platform**)
            - текущая рабочая директория (**cwd**)
            - окружение (**env**)
        - **process** — информация о процессе приложения:
            - идентификатор процесса (**pid**)
            - нагрузка CPU в процентах (**cpu_percent**)
            - используемая память в МБ (**memory_mb**)
            - количество потоков (**threads**)
        - **system** — информация о системе:
            - количество CPU (**cpu_count**)
            - общий объём памяти в ГБ (**total_memory_gb**)
            - доступный объём памяти в ГБ (**available_memory_gb**)
        - **metrics** — метрики сервиса:
            - количество обработанных запросов (**request_count**)
            - время работы сервиса в секундах (**uptime_seconds**)
        - Временная метка генерации данных (UTC) (**timestamp**)
    - Пример использования: локальная отладка, проверка загрузки процесса и состояния системы.
    """
    if os.getenv("ENVIRONMENT") == "production":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "Debug endpoint is disabled in production"},
        )

    process = psutil.Process()

    return {
        "environment": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "cwd": os.getcwd(),
            "env": os.getenv("ENVIRONMENT", "development"),
        },
        "process": {
            "pid": process.pid,
            "cpu_percent": round(process.cpu_percent(interval=0.1), 2),
            "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
            "threads": process.num_threads(),
        },
        "system": {
            "cpu_count": psutil.cpu_count(),
            "total_memory_gb": round(
                psutil.virtual_memory().total / 1024 / 1024 / 1024, 2
            ),
            "available_memory_gb": round(
                psutil.virtual_memory().available / 1024 / 1024 / 1024, 2
            ),
        },
        "metrics": {
            "request_count": request_count,
            "uptime_seconds": round(time.time() - start_time, 2),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
