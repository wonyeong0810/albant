from dotenv import load_dotenv
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import os
from random import randint
from uuid import uuid4
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from model import User, DepartmentEnum
from schemes import UserCreate, VerificationCodeModel
from repositories.user_repository import UserRepository

load_dotenv()

class RegisterService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=int(os.getenv("MAIL_PORT")),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
            MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
            USE_CREDENTIALS=True
        )

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def register_user(self, user: UserCreate, background_tasks: BackgroundTasks, db: Session):
        db_user = self.user_repository.get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        department_enum = DepartmentEnum(user.department) if user.department else None
        hashed_password = self.pwd_context.hash(user.password)
        verification_code = randint(100000, 999999)
        new_user = User(
            user_id=str(uuid4()),
            username=user.username,
            password=hashed_password,
            email=user.email,
            created_date=datetime.now(timezone.utc),
            modified_date=datetime.now(timezone.utc),
            department=department_enum,
            year=user.year,
            profile_pathname=user.profile_pathname,
            is_active=False,
            verification_code=verification_code
        )
        self.user_repository.create_user(db, new_user)

        message = MessageSchema(
            subject="Email Verification Code",
            recipients=[new_user.email],
            body=f"Your verification code is {verification_code}. Please enter this code to verify your email.",
            subtype="plain"
        )

        fm = FastMail(self.conf)
        background_tasks.add_task(fm.send_message, message)

        return new_user

    async def verify_email(self, verification: VerificationCodeModel, db: Session):
        user = self.user_repository.get_user_by_email(db, verification.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_active:
            raise HTTPException(status_code=400, detail="Email already verified")
        if user.verification_code != verification.code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

        user.is_active = True
        user.verification_code = None
        self.user_repository.update_user(db, user)
        return {"message": "Email verified successfully"}

    async def login_for_access_token(self, form_data, db: Session):
        user = self.user_repository.get_user_by_username(db, form_data.username)
        if not user or not self.pwd_context.verify(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Email not verified")

        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        # access_token = self.create_access_token(
        #     data={"sub": user.username}, expires_delta=access_token_expires
        # )
        access_token = self.create_access_token(
            data={"sub": user.user_id}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
        user = self.user_repository.get_user_by_id(db, user_id)
        if user is None:
            raise credentials_exception
        return user
