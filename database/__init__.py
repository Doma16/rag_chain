from sqlmodel import create_engine, Session, select
from database.models import UserCreate, UserRead, User, Token

DATABASE_URL = "sqlite:///users.db"


def get_engine():
    return create_engine(DATABASE_URL, echo=True)


def get_session(engine):
    with Session(engine) as session:
        yield session


def get_user_by_username(session: Session, username: str):
    query = select(User).where(User.username == username)
    return session.exec(query).first()
