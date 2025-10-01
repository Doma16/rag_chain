from typing import  Optional

from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    filename: str
    content: str

class UserQuery(BaseModel):
    username: str
    password: str

class UserPayLoad(BaseModel):
    username: str
    exp: int

class UserRead(BaseModel):
    id: int
    username: str
    password: str

class DocumentQuery(BaseModel):
    filename: str
    content: str