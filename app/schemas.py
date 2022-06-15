from pydantic import BaseModel
from pydantic.networks import EmailStr


class User_Request(BaseModel):
    username: str
    email: EmailStr
    password: str
    message: str


class User_Response(BaseModel):
    id: int
    username: str
    message: str

    class Config:
        orm_mode = True
