import logging
from logging.handlers import RotatingFileHandler
from app.core.config import BASE_DIR

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def create_file_handler(level: int = logging.INFO):
    # Файловый хэндлер
    log_file = LOGS_DIR / "app.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 МБ
        backupCount=2,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    return file_handler


def create_console_handler(level: int = logging.INFO):
    # Консольный хэндлер
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    return console_handler


def setup_logging(
    level: int = logging.INFO,
    file_level: int = logging.INFO,
    console_level: int = logging.INFO,
) -> None:
    """Настройка логирования для приложения"""
    root_logger = logging.getLogger()

    # Проверяем, не настроено ли уже логирование
    if root_logger.handlers:
        return  # Логирование уже настроено

    # Настройка уровня логирования
    root_logger.setLevel(level)

    file_handler = create_file_handler(file_level)
    console_handler = create_console_handler(console_level)
    # Добавляем хэндлеры
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.getLogger("sqlalchemy.engine.Engine").propagate = False


def get_logger(name: str) -> logging.Logger:
    """Получить логгер с указанным именем"""
    return logging.getLogger(name)


logger = logging.getLogger(__name__)
