from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import Users
from webapps.auth.forms import LoginForm, RegisterForm
from apis.routes.route_login import login_for_access_token, get_if_user
from db.repository.user import create_new_user
from schemes.user import UserCreate


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request, account: Users = Depends(get_if_user)):
    if account:
        return RedirectResponse("/")
    return templates.TemplateResponse("auth/login.html", {"request": request, "account": account})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successfully")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect username or password")
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/register/")
def register(request: Request, account: Users = Depends(get_if_user)):
    if account:
        return RedirectResponse("/")
    return templates.TemplateResponse("auth/register.html", {"request": request, "account": account})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db), account: Users = Depends(get_if_user)):
    form = RegisterForm(request)
    form_to_pass = form.__dict__
    form_to_pass["account"] = account
    await form.load_data(db=db)
    if await form.is_valid():
        try:
            response = templates.TemplateResponse("auth/login.html",
                                                  {"request": request, "msg": "Register Successfully"})
            create_new_user(UserCreate(username=form.username, email=form.email, password=form.password), db=db)
            return response
        except:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Enter valid Email please.")
    return templates.TemplateResponse("auth/register.html", form_to_pass)


@router.get("/logout")
def logout(request: Request, account: Users = Depends(get_if_user)):
    if account:
        response = templates.TemplateResponse("auth/logout.html", {"request": request})
        response.delete_cookie('access_token')
        return response
    return RedirectResponse("/")
