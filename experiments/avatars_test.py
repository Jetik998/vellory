
# Аватар берется из зависимости
# async def get_avatar_file(username) -> tuple[Path, str]:
#     # Получить итератор найденных файлов
#     files = list(AVATAR_DIR.glob(f"{username}*"))
#     # Получить первый файл из списка
#     file = files[0]
#     # Получить расширение файла например .jpg
#     ext = file.suffix.lower()
##
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
