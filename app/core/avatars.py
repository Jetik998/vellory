from pathlib import Path
from fastapi import UploadFile, HTTPException
import aiofiles

from app.core.config import BASE_DIR

AVATAR_DIR = BASE_DIR / "app" / "media" / "avatars"
AVATAR_DIR.mkdir(exist_ok=True)


async def save_avatar_file(username: str, file: UploadFile) -> str:
    ext = Path(file.filename).suffix.lower()

    if ext not in {".jpg", ".jpeg", ".png"}:
        raise HTTPException(
            status_code=400, detail="Only JPG and PNG files are allowed"
        )

    for existing_file in AVATAR_DIR.glob(f"{username}*"):
        existing_file.unlink(missing_ok=True)

    path = AVATAR_DIR / f"{username}{ext}"

    async with aiofiles.open(path, "wb") as f:
        await f.write(await file.read())

    return path.name
