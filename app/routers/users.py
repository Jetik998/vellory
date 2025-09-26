from fastapi import APIRouter, HTTPException
from app.crud.users import db_get_user, db_user_exists, db_add_user
from security.password import verify_password
from app.shemas.users import Register
from app.dependencies import SessionDep


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", summary="Регистрация пользователя")
async def register(user: Register, session: SessionDep):
    db_user = db_user_exists(user.username, session)
    if db_user:  # Если db_user не False, значит такой пользователь уже существует
        raise HTTPException(status_code=400, detail="Username already exists")
    await db_add_user(user, session)
    return {"message": "User created successfully"}


@router.post("/login", summary="Вход в систему и выдача токена")
async def login(user: Register, session: SessionDep):
    db_user = await db_get_user(user.username, session)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    verify_result = verify_password(user.password, db_user.hashed_password)
    if not verify_result:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    pass
