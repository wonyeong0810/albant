#model.py
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from datetime import datetime, timezone
from uuid import uuid4

class DepartmentEnum(PyEnum):
    SOFTWARE = 1
    HACKING = 2
    CONTENT_DESIGN = 3
    IT_MANAGEMENT = 4

class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(255), primary_key=True, index=True)
    username = Column(String(10), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    point = Column(Integer)
    profile_pathname = Column(String(255))
    password = Column(String(255), nullable=False)
    department = Column(Enum(DepartmentEnum), nullable=True)  # Here, sqlalchemy.Enum is used
    year = Column(Integer)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    modified_date = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=False)
    # Define the one-to-many relationship
    transaction_posts = relationship("TransactionPost", back_populates="user")


class TransactionPost(Base):
    __tablename__ = "transaction_post"
    transaction_post_id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("user.user_id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(String(5000), nullable=False)
    deadline = Column(Date, nullable=True)
    point = Column(Integer, nullable=False)
    tag = Column(String(255), nullable=True)
    image_pathname = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))

    # Define the many-to-one relationship
    user = relationship("User", back_populates="transaction_posts")
