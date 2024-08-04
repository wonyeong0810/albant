from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext

from database import SessionLocal, engine, database
from model import Base, User
from schemas import UserCreate, UserOut

# 데이터베이스 테이블 생성 (필요한 경우)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register/", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        user_id=user.username,  # Example: username as user_id
        username=user.username,
        password=hashed_password,
        created_date=datetime.now(),
        modified_date=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and pwd_context.verify(user.password, db_user.password):
        return {"message": "Login successful!"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/users/{username}", response_model=UserOut)
async def read_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
