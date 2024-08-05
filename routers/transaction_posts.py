# routers/transaction_posts
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from uuid import uuid4

from database import SessionLocal
from model import TransactionPost
from schemes import TransactionPostCreate, TransactionPostUpdate, TransactionPostOut

transaction_posts_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TransactionPost CRUD 기능 추가

@transaction_posts_router.post("/transaction_posts/", response_model=TransactionPostOut)
def create_transaction_post(post: TransactionPostCreate, db: Session = Depends(get_db)):
    db_post = TransactionPost(
        transaction_post_id=str(uuid4()),
        user_id=post.user_id,
        title=post.title,
        content=post.content,
        deadline=post.deadline,
        point=post.point,
        tag=post.tag,
        image_pathname=post.image_pathname,
        created_date=datetime.now(timezone.utc)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@transaction_posts_router.get("/transaction_posts/{post_id}", response_model=TransactionPostOut)
def read_transaction_post(post_id: str, db: Session = Depends(get_db)):
    db_post = db.query(TransactionPost).filter(TransactionPost.transaction_post_id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@transaction_posts_router.get("/transaction_posts/", response_model=list[TransactionPostOut])
def read_transaction_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(TransactionPost).offset(skip).limit(limit).all()
    return posts

@transaction_posts_router.put("/transaction_posts/{post_id}", response_model=TransactionPostOut)
def update_transaction_post(post_id: str, post: TransactionPostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(TransactionPost).filter(TransactionPost.transaction_post_id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict(exclude_unset=True).items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

@transaction_posts_router.delete("/transaction_posts/{post_id}", response_model=TransactionPostOut)
def delete_transaction_post(post_id: str, db: Session = Depends(get_db)):
    db_post = db.query(TransactionPost).filter(TransactionPost.transaction_post_id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return db_post

