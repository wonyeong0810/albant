from pydantic import BaseModel
from datetime import date, datetime

# 사용자 생성을 위한 스키마
class UserCreate(BaseModel):
    username: str
    password: str

# 사용자 읽기를 위한 스키마
class UserOut(BaseModel):
    username: str
    user_id: str  # user_id 반환 필요성에 따라 포함

    class Config:
        orm_mode = True

class TransactionPostBase(BaseModel):
    user_id: str
    title: str
    content: str
    deadline: date | None = None
    point: int
    tag: str | None = None
    image_pathname: str | None = None

class TransactionPostCreate(TransactionPostBase):
    pass

class TransactionPostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    deadline: date | None = None
    point: int | None = None
    tag: str | None = None
    image_pathname: str | None = None

class TransactionPostOut(TransactionPostBase):
    transaction_post_id: str
    created_date: datetime

    class Config:
        orm_mode = True