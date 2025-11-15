import aiofiles.os
import secrets
from pathlib import Path
from fastapi import HTTPException
import aiofiles

from app.core.config import BASE_DIR

AVATAR_DIR = BASE_DIR / "app" / "media" / "avatars"
AVATAR_DIR.mkdir(exist_ok=True)


async def update_avatar_file(file) -> str:
    # Получаем расширение файла example.jpg > .jpg
    ext = Path(file.filename).suffix.lower()
    file_size = 5 * 1024 * 1024  # 5 MB

    # Проверяем что расширение есть в списке.
    if ext not in {".jpg", ".jpeg", ".png", ".svg"}:
        raise HTTPException(
            status_code=400, detail="Only JPG, SVG, JPEG, and PNG files are allowed"
        )

    content = await file.read()
    if len(content) > file_size:
        raise HTTPException(400, "Слишком тяжелый файл. Максимально 5 MB")

    # Создаем имя файла + расширение и путь до нового файла например ~/2c1e7b98f20.jgp
    filename = secrets.token_hex(16) + ext
    path = AVATAR_DIR / filename

    # Открыть файл и записать данные
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)

    # Возвращает путь к файлу
    return filename


async def delete_avatar_file(filename: str):
    if not filename:
        return
    path = AVATAR_DIR / filename
    if path.exists():
        try:
            await aiofiles.os.remove(path)
        except Exception:
            pass  # Не роняем приложение, если файл уже отсутствует


# Аватар берется из зависимости
# async def get_avatar_file(username) -> tuple[Path, str]:
#     # Получить итератор найденных файлов
#     files = list(AVATAR_DIR.glob(f"{username}*"))
#     # Получить первый файл из списка
#     file = files[0]
#     # Получить расширение файла например .jpg
#     ext = file.suffix.lower()
#
#     if ext in [".jpg", ".jpeg"]:
#         media_type = "image/jpeg"
#     elif ext == ".png":
#         media_type = "image/png"
#     elif ext == ".svg":
#         media_type = "image/svg+xml"
#     else:
#         media_type = "application/octet-stream"
#
#     return file, media_type
