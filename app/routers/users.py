from app.core.dependencies import CurrentUserDep, SessionDep
from app.crud.users import db_get_user, db_update_user_avatar
from app.enums import Tags
from app.schemas.users import AvatarUpdateResponse
from fastapi import APIRouter, status, UploadFile, File, Request

router = APIRouter(prefix="/users", tags=[Tags.users])

@router.post(
    "/avatar",
    summary="Загрузка аватара",
    status_code=status.HTTP_201_CREATED,
    response_model=AvatarUpdateResponse,
)
async def upload_avatar(
    request: Request,
    user: CurrentUserDep,
    session: SessionDep,
    file: UploadFile = File(...),
) -> AvatarUpdateResponse:
    base_url = str(request.base_url).rstrip("/")
    db_user = await db_get_user(user.username, session)
    updated_user = await db_update_user_avatar(file, db_user, session)
    return AvatarUpdateResponse(
        message="Avatar updated", avatar_url=f"{base_url}/avatars/{updated_user.avatar}"
    )
