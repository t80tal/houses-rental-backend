from fastapi.security import OAuth2PasswordRequestForm
from apis.utils import OAuth2PasswordBearerWithCookie
from fastapi import Depends, HTTPException, status, Response, APIRouter, Request
from jose import jwt, JWTError
from db.session import get_db
from db.models.users import Users
from sqlalchemy.orm import Session
from core.config import settings
from datetime import timedelta
from core.security import create_access_token
from db.repository.user import get_user
from fastapi.security.utils import get_authorization_scheme_param
from core.hashing import Hasher

router = APIRouter()


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token")
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password."))
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expire)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Couldn't validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


def get_if_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(token)
        return get_current_user_from_token(token=param, db=db)
    except Exception as e:
        return False
