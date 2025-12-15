# class RouterResponse:
#     def __init__(self, router_path="", deps: list[str] = None):
#         self.router_path = router_path
#         self.deps = deps or []
#         self.exceptions = set()
#         self.status_codes = []
#         self.responses_ru = {}
#         self.responses_en = {}
#
#         self.init_exceptions()
#         self.init_status_codes()
#         self.init_responses()
#
#     def init_exceptions(self):
#         if self.deps:
#             for dep in self.deps:
#                 for exception in dependency_exceptions[dep]:
#                     self.exceptions.add(exception)
#
#     def init_status_codes(self):
#         if self.exceptions:
#             for exception in self.exceptions:
#                 self.status_codes.append(exception.status_code)
#
#     def init_responses(self):
#         if self.status_codes:
#             for code in self.status_codes:
#                 if code in DESCRIPTIONS:
#                     self.responses_ru[code] = {
#                         "model": MODELS.get(code, ErrorResponse),
#                         "description": DESCRIPTIONS[code].get(DESCRIPTIONS[code]["ru"])
#                     }
#                     self.responses_en[code] = {
#                         "model": MODELS.get(code, ErrorResponse),
#                         "description": DESCRIPTIONS[code].get(DESCRIPTIONS[code]["en"])
#                     }
#
#     def __repr__(self):
#         return (f"RouterResponse(router_path={self.router_path!r}, "
#                 f"deps={self.deps!r}, "
#                 f"exceptions={self.exceptions!r}, "
#                 f"status_codes={self.status_codes!r}, "
#                 f"responses_ru={self.responses_ru!r}, "
#                 f"responses_en={self.responses_en!r})")
#
# class CreateTask(RouterResponse):
#     pass
#
# create_task = CreateTask("create_task", ["SessionDep", "CurrentUserDep"])
#
# print(create_task)
#
# def get_response_in_code(code: int, lang="ru") -> Dict[str, Any] :
#     result = {}
#     for code in codes:
#         if code in DESCRIPTIONS:
#             result[code] = {
#                 "model": MODELS.get(code, ErrorResponse),
#                 "description": DESCRIPTIONS[code].get(lang, DESCRIPTIONS[code]["ru"])
#             }
#     return result
#
#
# #Возвращает коды ошибок у зависимостей
# class CustomResponses:
#     def __init__(self, deps, exceptions: list[CustomException | None] = None):
#         self.dep = dep
#         self.exceptions = exceptions or []
#         self.status_codes = []
#
#     def init_status_codes(self):
#         codes = []
#         for exception in self.exceptions:
#             codes.append(exception.status_code)
#         self.status_codes = codes
#
#     def get_codes_list(self):
#         return self.status_codes
#
# class CurrentUserFromCookieRefreshLenient(BaseDep):
#     pass
#
# class SessionDep(BaseDep):
#     pass
#
#
#
#
# class Deps:
#     def __init__(self):
#         self.exceptions = (
#             NotFoundException,
#             ForbiddenException,
#             UnauthorizedException,
#             UnprocessableEntityException,
#             DuplicateValueException,
#             RateLimitException
#         )
#
# def exceptions_for_deps(dep) -> list[CustomException]:
#     return x[dep]
#
# def code_for_exception(exeption) -> str | None:
#     return exeption.get_status_code
#
#
