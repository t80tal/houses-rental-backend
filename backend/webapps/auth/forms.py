from fastapi import Request, Depends
from typing import Optional, List
from db.session import get_db
from sqlalchemy.orm import Session
from db.repository.user import check_if_mail_exists, check_if_username_exists


class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors: List = []
        self.password: str = None
        self.username: str = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not len(self.username) > 5:
            self.errors.append("A valid username is neccesary")
        if not self.password or not len(self.password) > 5:
            self.errors.append(("A valid password is neccesary"))
        if not self.errors:
            return True
        return False


class RegisterForm:
    def __init__(self, request: Request,db: Session = Depends(get_db)):
        self.request = request
        self.errors: List = []
        self.password: str = None
        self.email: str = None
        self.username: str = None
        self.db: Session = None

    async def load_data(self,db: Session):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        self.email = form.get("email")
        self.db = db

    async def is_valid(self):
        if not self.username or not len(self.username) > 5:
            self.errors.append("A valid username is neccesary.")
        if not self.password or not len(self.password) > 5:
            self.errors.append(("A valid password is neccesary."))
        if not self.email or not (self.email.__contains__('@')):
            self.errors.append(("A valid email is neccesary."))
        if check_if_mail_exists(self.email, self.db):
            self.errors.append(("Email already exists."))
        if check_if_username_exists(self.username, self.db):
            self.errors.append(("Username already exists."))
        if not self.errors:
            return True
        return False
