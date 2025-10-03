from jose import jwt, JWTError
from datetime import datetime, timedelta

EXPIRE_MINUTES = 15
SECRET_KEY = "JWT"


def create_token(data: dict):
    data["exp"] = datetime.now() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(data, SECRET_KEY)


def read_token(token):
    try:
        payload = jwt.decode(token, key=SECRET_KEY)
        return payload
    except JWTError:
        return None
