from pydantic import BaseModel

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
