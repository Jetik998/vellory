from decouple import config
from datetime import timedelta

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
EXP_MIN = timedelta(minutes=int(config("EXP_MIN")))
