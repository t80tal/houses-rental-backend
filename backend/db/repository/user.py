from sqlalchemy.orm import Session
from schemes.user import UserCreate
from db.models.users import Users
from datetime import datetime, date
from core.hashing import Hasher


def create_new_user(given_user: UserCreate, db: Session):
    user = Users(
        username=given_user.username,
        email=given_user.email,
        hashed_password=Hasher.get_password_hash(given_user.password),
        date_created=datetime.now().date(),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(username: str, db: Session):
    return db.query(Users).filter(Users.username == username).first()


def check_if_mail_exists(email: str, db: Session):  # for frontend messages.
    return db.query(Users).filter(Users.email == email).first()

def check_if_username_exists(username: str, db: Session):  # for frontend messages.
    return db.query(Users).filter(Users.username == username).first()
