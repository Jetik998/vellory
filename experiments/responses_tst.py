# from fastcrud.exceptions.http_exceptions import UnauthorizedException, NotFoundException
#
# from app.api.dependencies import CurrentUserDep, CurrentUserFromCookieRefreshLenient, SessionDep
# from app.schemas.responses import ErrorResponse
# from app.schemas.tasks import RequestTask
#
#
# # Словарь описаний на разных языках
# DESCRIPTIONS = {
#     400: {"ru": "Неверный запрос", "en": "Bad request"},
#     401: {"ru": "Пользователь не аутентифицирован", "en": "User is not authenticated"},
#     403: {"ru": "Недостаточно прав", "en": "Insufficient permissions"},
#     404: {"ru": "Ресурс не найден", "en": "Resource not found"},
#     422: {"ru": "Невозможно обработать запрос", "en": "Unprocessable entity"},
#     429: {"ru": "Превышен лимит запросов", "en": "Rate limit exceeded"},
#     500: {"ru": "Внутренняя ошибка сервера", "en": "Internal server error"},
# }
#
# # Словарь моделей (если нужно для разных кодов можно расширить)
# MODELS = {
#     400: ErrorResponse,
#     401: ErrorResponse,
#     403: ErrorResponse,
#     404: ErrorResponse,
#     422: ErrorResponse,
#     429: ErrorResponse,
#     500: ErrorResponse,
# }
#
# EXCEPTION_CODE = {
#     "BadRequestException": 400,
#     "UnauthorizedException": 401,
#     "ForbiddenException": 403,
#     "NotFoundException": 404,
#     "UnprocessableEntityException": 422,
#     "DuplicateValueException": 422,
#     "RateLimitException": 429,
#     "InternalServerErrorException": 500,
# }
#
#
# dependency_exceptions = {
#     "CurrentUserFromCookieRefreshLenient": ["UnauthorizedException", "NotFoundException"],
#     "SessionDep": ["NotFoundException"],
#     "CurrentUserDep": ["UnauthorizedException", "NotFoundException"],
# }
#
# dependency_codes = {
#     "CurrentUserFromCookieRefreshLenient": [EXCEPTION_CODE[exception] for exception in dependency_exceptions["CurrentUserFromCookieRefreshLenient"]],
# }
#
