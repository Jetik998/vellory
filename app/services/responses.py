from typing import List, Dict, Type
from app.schemas.responses import ErrorResponse
from app.core.exceptions import (
    UnauthorizedException,
    NotFoundException,
    RateLimitException,
)


class DependencyResponseConfig:
    def __init__(self, exceptions: List[Type[Exception]], model: Type = ErrorResponse):
        self.exceptions = exceptions
        self.model = model

    @property
    def codes(self) -> List[int]:
        return [exc.code for exc in self.exceptions]

    @property
    def responses(self, lang="ru") -> Dict[int, Dict[str, any]]:
        return {
            exc.code: {
                "model": self.model,
                "description": (
                    exc.description_ru if lang == "ru" else exc.description_en
                ),
            }
            for exc in self.exceptions
        }


class Dependencies:
    CurrentUserDep = DependencyResponseConfig(
        [
            UnauthorizedException,
            NotFoundException,
        ]
    )
    CurrentUserFromCookieRefreshLenient = DependencyResponseConfig(
        [
            UnauthorizedException,
            NotFoundException,
        ]
    )
    SessionDep = DependencyResponseConfig([NotFoundException])
    rate_limiter = DependencyResponseConfig([RateLimitException])


base_responses_api = {
    **Dependencies.CurrentUserDep.responses,
    **Dependencies.SessionDep.responses,
    **Dependencies.rate_limiter.responses,
}

base_responses_web = {
    **Dependencies.CurrentUserFromCookieRefreshLenient.responses,
    **Dependencies.SessionDep.responses,
    **Dependencies.rate_limiter.responses,
}


base_responses_codes = [
    Dependencies.CurrentUserDep.codes,
    Dependencies.SessionDep.codes,
]
