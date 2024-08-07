from sqlalchemy.orm import Session
from model import User

class UserRepository:
    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, db: Session, id: str):
        return db.query(User).filter(User.user_id == id).first()

    def create_user(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_user(self, db: Session, user: User):
        db.commit()
        db.refresh(user)
        return user
