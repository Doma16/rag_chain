from sqlmodel import create_engine, Session, select
from database.models import User, Document
from database.models import UserQuery, UserPayLoad, UserRead  # noqa: F401
from database.models import DocumentQuery  # noqa: F401

DATABASE_URL = "sqlite:///users.db"
ENGINE = create_engine(DATABASE_URL, echo=True)


def get_engine():
    return ENGINE


def get_session():
    with Session(ENGINE) as session:
        yield session


def get_user_by_username(session: Session, username: str):
    query = select(User).where(User.username == username)
    return session.exec(query).first()


def get_user_documents(session: Session, user_id: int):
    query = select(Document).where(Document.user_id == user_id)
    return session.exec(query).all()

def get_document(session: Session, doc_id: int):
    query = select(Document).where(Document.id == doc_id)
    return session.exec(query).first()
