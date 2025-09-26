from decouple import config
from datetime import datetime, timedelta, timezone
import jwt


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
