
# Аватар берется из зависимости
# @router.get(
#     "/avatar/get",
#     response_class=FileResponse,
# )
# async def get_avatar(
#     user: CurrentUserFromCookieRefreshLenient,
# ) -> FileResponse:
#
#     # поиск файла по маске
#     avatar, media_type = await get_avatar_file(user.username)
#
#     if avatar is None:
#         raise HTTPException(status_code=404, detail="Avatar not found")
#
#     return FileResponse(avatar, media_type=media_type)
