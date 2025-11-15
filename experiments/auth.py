#
# async def get_user_email(request: Request) -> str:
#     """
#     Извлекает и проверяет корректность JWT access-токена из cookies запроса.
#
#     Параметры
#     ----------
#     request : Request
#         Объект запроса FastAPI, содержащий cookies.
#
#     Возвращает
#     ----------
#     str
#         Валидный JWT access-токен.
#
#     Исключения
#     ----------
#     UnauthorizedException
#         Если токен отсутствует, недействителен, имеет неверный тип или срок его действия истёк.
#     """
#     token = request.cookies.get("access_token")
#
#     if not token:
#         raise UnauthorizedException("Access token missing.")
#
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if not payload.get("sub") or payload.get("token_type") != TokenType.ACCESS:
#             raise UnauthorizedException("Invalid access token type.")
#     except ExpiredSignatureError:
#         raise UnauthorizedException("Access token has expired.")
#     except InvalidTokenError:
#         raise UnauthorizedException("Invalid access token.")
#
#     return token
#
# async def get_current_userr(request: Request, session: SessionDep) -> TokenData:
#     email = get_user_email(request)
#     user = db_get_user(session, email=email)
#
#
# GetAccessToken = Annotated[str | None, Depends(get_valid_access_token)]
# response_tokens

    #
    # access_token = tokens["access_token"]
    # refresh_token = tokens["refresh_token"]
    #
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=60 * 60,
    # )
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=60 * 60 * 2,  # 7 дней
    # )
    #
    # return {
    #     "access_token": "created",
    #     "refresh_token": "created",
    # }


# @router.get(
#     "/",
#     summary="Главная страница",
#     description="Возвращает HTML-файл главной страницы, если пользователь авторизован с помощью access_token из cookie.",
# )
# async def home(user: CurrentUserFromCookieAccess):
#     """
#     Возвращает главную страницу приложения для авторизованного пользователя.
#
#     Параметры
#     ----------
#     user : CurrentUserFromCookie
#         Объект пользователя, извлечённый из базы данных.
#         Данные о пользователе получены из access_token, сохранённого в cookie.
#
#     Возвращает
#     -------
#     FileResponse
#         HTML-файл главной страницы при успешной аутентификации.
#
#     Исключения
#     ----------
#     UnauthorizedException
#         Если отсутствует или недействителен токен авторизации.
#     NotFoundException
#         Если пользователь, указанный в токене, не найден в базе данных.
#     """
#     return FileResponse(TEMPLATES / "index.html")
