from jose import jwt
from datetime import datetime, timedelta

EXPIRE_MINUTES = 15
SECRET_KEY = "JWT"


def create_token(data: dict):
    data["exp"] = datetime.now() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(data, SECRET_KEY)
