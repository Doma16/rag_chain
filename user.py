from jwt import read_token
from database import get_user_by_username, UserPayLoad, UserRead

def get_user(session, token):
    payload = UserPayLoad(**read_token(token))
    user = get_user_by_username(session, payload.username)
    return UserRead(**user.model_dump())
