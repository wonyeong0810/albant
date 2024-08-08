# transaction_posts.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from schemes import TransactionPostCreate, TransactionPostOut, TransactionPostUpdate
from services.transaction_post_service import TransactionPostService

def get_db():
    db = SessionLocal()
    try:
        yield 
    finally:
        db.close()

transaction_posts_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

db: Session = Depends(get_db)
service = TransactionPostService(db)

@transaction_posts_router.post("/", response_model=TransactionPostOut)
async def create_post(post: TransactionPostCreate, token: str = Depends(oauth2_scheme)):
    # service = TransactionPostService(db)
    user_id = await service.get_current_user(token, db)
    return await service.create_transaction_post(post, user_id)

@transaction_posts_router.get("/{post_id}", response_model=TransactionPostOut)
async def read_post(post_id: str):
    # service = TransactionPostService(db)
    db_post = await service.get_transaction_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@transaction_posts_router.put("/{post_id}", response_model=TransactionPostOut)
async def update_post(post_id: str, post: TransactionPostUpdate):
    # service = TransactionPostService(db)
    db_post = await service.update_transaction_post(post_id, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@transaction_posts_router.delete("/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    # service = TransactionPostService(db)
    deleted = await service.delete_transaction_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

@transaction_posts_router.get("/", response_model=List[TransactionPostOut])
async def read_all_posts():
    # service = TransactionPostService(db)
    return await service.get_all_transaction_posts()
