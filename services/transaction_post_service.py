# transaction_post_service.py

import os
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
from schemes import TransactionPostCreate, TransactionPostUpdate
from model import TransactionPost
from repositories.transaction_post_repository import TransactionPostRepository

load_dotenv()

class TransactionPostService:
    def __init__(self, db: Session):
        self.repository = TransactionPostRepository(db)
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")

    async def create_transaction_post(self, post: TransactionPostCreate, user_id : str) -> TransactionPost:
        return self.repository.create_post(post, user_id)

    async def get_transaction_post(self, post_id: str) -> TransactionPost:
        return self.repository.get_post(post_id)

    async def update_transaction_post(self, post_id: str, post: TransactionPostUpdate) -> TransactionPost:
        return self.repository.update_post(post_id, post)

    async def delete_transaction_post(self, post_id: str) -> bool:
        return self.repository.delete_post(post_id)

    async def get_all_transaction_posts(self) -> list[TransactionPost]:
        return self.repository.get_all_posts()
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
        # user = self.user_repository.get_user_by_id(db, user_id)
        # if user is None:
        #     raise credentials_exception
        return user_id
