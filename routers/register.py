from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemes import UserCreate, VerificationCodeModel
from services.user_service import RegisterService
from database import SessionLocal

register_router = APIRouter()
register_service = RegisterService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@register_router.post("/", response_model=UserCreate)
async def register(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return await register_service.register_user(user, background_tasks, db)

@register_router.post("/verify-email", response_model=dict)
async def verify_email(verification: VerificationCodeModel, db: Session = Depends(get_db)):
    return await register_service.verify_email(verification, db)

@register_router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await register_service.login_for_access_token(form_data, db)

@register_router.get("/users/me", response_model=UserCreate)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await register_service.get_current_user(token, db)
