import pydantic

class User(pydantic.BaseModel):
    name: str
    password: str
