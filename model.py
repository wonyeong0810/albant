# model.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(255), primary_key=True)
    username = Column(String(10), unique=True, nullable=False)
    point = Column(Integer)
    profile_pathname = Column(String(255))
    password = Column(String(255), nullable=False)
    department = Column(Integer)
    year = Column(Integer)
    created_date = Column(DateTime)
    modified_date = Column(DateTime)

class TransactionPost(Base):
    __tablename__ = 'transaction_post'
    transaction_post_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey('user.user_id'))
    title = Column(String(500))
    content = Column(String(5000))
    deadline = Column(DateTime)
    point = Column(Integer)
    tag = Column(String(255))
    image_pathname = Column(String(255))
    created_date = Column(DateTime)
    user = relationship("User", back_populates="posts")

User.posts = relationship("TransactionPost", order_by=TransactionPost.transaction_post_id, back_populates="user")

# 나머지 클래스도 이와 유사하게 작성
