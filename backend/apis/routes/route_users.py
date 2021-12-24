from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from db.session import get_db
from schemes.user import UserCreate, ShowUser
from db.repository.user import create_new_user, get_user

router = APIRouter()


@router.post("/create", response_model=ShowUser)
def create_user(given_user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(given_user=given_user, db=db)

