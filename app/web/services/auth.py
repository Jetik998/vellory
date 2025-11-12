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
