from datetime import datetime

from pydantic import BaseModel


class Login(BaseModel):
    user_name: str
    password: str


class ZhuCe(BaseModel):
    user_name: str
    password: str
    phone: str
    birthdata: str
    token:str