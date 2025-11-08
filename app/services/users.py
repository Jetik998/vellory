from fastapi import HTTPException, status

from app.api.dependencies import SessionDep
from app.crud.users import db_user_name_exists, db_user_email_exists, db_add_user
from app.schemas.users import UserIn, UserRegisterResponse


async def register_user(user: UserIn, session: SessionDep) -> UserRegisterResponse:
    if await db_user_name_exists(user.username, session) or await db_user_email_exists(
        str(user.email), session
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        )

    await db_add_user(user, session)
    return UserRegisterResponse(
        username=user.username, message="User registered successfully"
    )
