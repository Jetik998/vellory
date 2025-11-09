from decouple import config
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # корень проекта
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
EXP_MIN = timedelta(minutes=int(config("EXP_MIN")))
