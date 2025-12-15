from typing import Union
from http import HTTPStatus
from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Union[str, None] = None,
    ):
        if not detail:  # pragma: no cover
            detail = HTTPStatus(status_code).description
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(CustomException):
    code = 400
    description_ru = "Неверный запрос"
    description_en = "Bad request"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )  # pragma: no cover


class NotFoundException(CustomException):
    code = 404
    description_ru = "Ресурс не найден"
    description_en = "Resource not found"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail
        )  # pragma: no cover


class ForbiddenException(CustomException):
    code = 403
    description_ru = "Недостаточно прав"
    description_en = "Insufficient permissions"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail
        )  # pragma: no cover


class UnauthorizedException(CustomException):
    code = 401
    description_ru = "Пользователь не аутентифицирован"
    description_en = "User is not authenticated"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
        )  # pragma: no cover


class UnprocessableEntityException(CustomException):
    code = 422
    description_ru = "Ошибка валидации данных"
    description_en = "Unprocessable entity"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )  # pragma: no cover


class DuplicateValueException(CustomException):
    code = 422
    description_ru = "Ошибка валидации данных"
    description_en = "Unprocessable entity"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class RateLimitException(CustomException):
    code = 429
    description_ru = "Превышен лимит запросов"
    description_en = "Rate limit exceeded"

    def __init__(self, detail: Union[str, None] = None):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail
        )  # pragma: no cover
