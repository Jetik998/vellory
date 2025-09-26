from decouple import config
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status

SECRET_KEY = config("SECRET_KEY")
EXP_MIN = timedelta(config("EXP_MIN"))


def create_token(user_id, username):
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": now + timedelta(hours=1),  # Токен действителен 1 час
        "iat": now,
        "nbf": now,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
