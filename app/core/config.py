from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # корень проекта
ENV_DIR = BASE_DIR / ".env"
WEB_DIR = BASE_DIR / "app" / "web" / "templates"
TEMPLATES = BASE_DIR / WEB_DIR
ICON_DIR = BASE_DIR / "app" / "media" / "img"


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    EXP_MIN: int

    RATE_LIMIT_TIMES: int
    RATE_LIMIT_SECONDS: int

    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_SECONDS: int

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def redis_url(self) -> str:
        password_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(
        env_file=ENV_DIR,
    )


settings = Settings()
