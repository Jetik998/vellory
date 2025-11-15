from pathlib import Path
from fastapi import HTTPException
import aiofiles

from app.core.config import BASE_DIR

AVATAR_DIR = BASE_DIR / "app" / "media" / "avatars"
AVATAR_DIR.mkdir(exist_ok=True)


async def update_avatar_file(username: str, file) -> str:
    # Получаем расширение файла example.jpg > .jpg
    ext = Path(file.filename).suffix.lower()

    # Проверяем что расширение есть в списке.
    if ext not in {".jpg", ".jpeg", ".png", ".svg"}:
        raise HTTPException(
            status_code=400, detail="Only JPG, SVG, JPEG, and PNG files are allowed"
        )

    # Поиск и удаление существующего аватара
    for existing_file in AVATAR_DIR.glob(f"{username}*"):
        existing_file.unlink(missing_ok=True)
    # путь до нового файла например ~/user.jgp
    path = AVATAR_DIR / f"{username}{ext}"

    # Открыть файл и записать данные
    async with aiofiles.open(path, "wb") as f:
        await f.write(await file.read())

    # Возвращает только имя файла
    return path.name


async def get_avatar_file(username) -> tuple[Path, str]:
    # Получить итератор найденных файлов
    files = list(AVATAR_DIR.glob(f"{username}*"))
    # Получить первый файл из списка
    file = files[0]
    # Получить расширение файла например .jpg
    ext = file.suffix.lower()

    if ext in [".jpg", ".jpeg"]:
        media_type = "image/jpeg"
    elif ext == ".png":
        media_type = "image/png"
    else:
        media_type = "application/octet-stream"

    return file, media_type
