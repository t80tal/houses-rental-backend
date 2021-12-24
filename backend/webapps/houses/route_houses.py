from fastapi import APIRouter, Request, Depends, HTTPException, status, responses, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import Users
from schemes.house import CreateHouse
from db.repository.house import list_houses, retrieve_house, create_new_house, get_houses_by_owner_id, \
    delete_house_by_id, update_house_by_id, list_false_houses, active_house_by_id, deactive_house_by_id
from webapps.houses.forms import HouseCreateForm
from fastapi.security.utils import get_authorization_scheme_param
from apis.routes.route_login import get_current_user_from_token, get_if_user

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), account: Users = Depends(get_if_user)):
    houses = list_houses(db=db)
    return templates.TemplateResponse("homepage.html", {"request": request, "houses": houses, "account": account})


@router.get("/details/{id}")
def house_detail(id: int, request: Request, db: Session = Depends(get_db), account: Users = Depends(get_if_user)):
    house = retrieve_house(id=id, db=db)
    if not house:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} does not exist"))
    return templates.TemplateResponse("houses/details.html",
                                      {"request": request, "house": house, "account": account})


@router.get("/sell")
def create_house(request: Request, account: Users = Depends(get_current_user_from_token)):
    return templates.TemplateResponse("houses/create-house.html", {"request": request, "account": account})


@router.post("/sell")
async def create_house_method(request: Request, db: Session = Depends(get_db), account: Users = Depends(get_if_user)):
    form = HouseCreateForm(request)
    form_to_pass = form.__dict__
    form_to_pass["account"] = account
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: Users = get_current_user_from_token(token=param, db=db)
            house = CreateHouse(**form.__dict__)
            house = create_new_house(given_house=house, db=db, owner_id=current_user.id)
            houses = list_houses(db=db)
            return responses.RedirectResponse(
                f"/details/{house.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            form_to_pass = form.__dict__
            form_to_pass["account"] = account
            return templates.TemplateResponse("houses/create-house.html", form_to_pass)
    return templates.TemplateResponse("houses/create-house.html", form_to_pass)


@router.get("/houses")
def show_your_houses(request: Request, account: Users = Depends(get_if_user),
                     db: Session = Depends(get_db)):
    if account:
        houses = get_houses_by_owner_id(id=account.id, db=db)
        return templates.TemplateResponse("houses/own_houses.html",
                                          {"request": request, "account": account, "houses": houses})
    return responses.RedirectResponse("/login")


@router.get("/delete/{id}")
def delete(id: int, request: Request, db: Session = Depends(get_db),
           account: Users = Depends(get_current_user_from_token)):
    house = retrieve_house(id=id, db=db)
    if not house:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} doesn't exist"))
    if house.owner_id == account.id or account.is_superuser:
        if delete_house_by_id(id=id, db=db, owner_id=account.id):
            houses = get_houses_by_owner_id(id=account.id, db=db)
            return templates.TemplateResponse("houses/own_houses.html",
                                              {"request": request, "account": account, "houses": houses,
                                               "msg": "Successfully Deleted."})

        else:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} doesn't exist"))
    raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted."))


@router.get("/update/{id}")
def update(id: int, request: Request, db: Session = Depends(get_db), account: Users = Depends(get_current_user_from_token)):
    house = retrieve_house(id=id, db=db)
    if house.owner_id == account.id or account.is_superuser:
        if not house:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} does not exist"))
        form_to_pass = {"request": request}
        form_to_pass.update(house.__dict__)
        form_to_pass.update({"account": account})
        return templates.TemplateResponse("houses/update-house.html", form_to_pass)
    raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted."))


@router.post("/update/{id}")
async def update(id: int, request: Request, db: Session = Depends(get_db), account: Users = Depends(get_current_user_from_token)):
    form = HouseCreateForm(request)
    form_to_pass = form.__dict__
    form_to_pass["account"] = account
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: Users = get_current_user_from_token(token=param, db=db)
            house = CreateHouse(**form.__dict__)
            house = update_house_by_id(id=id, house=house, db=db, current_user=current_user)
            form_to_pass.update({"msg": "Successfully Updated, Wait for admin to accept."})
            return templates.TemplateResponse("houses/update-house.html", form_to_pass)
        except Exception as e:
            form.__dict__.get("errors").append(
                "Error occured you might not permitted, If this error continues contact the admin."
            )
            form_to_pass = form.__dict__
            form_to_pass["account"] = account
            return templates.TemplateResponse("houses/update-house.html", form_to_pass)
    return templates.TemplateResponse("houses/update-house.html", form_to_pass)


@router.get("/manage-houses")
def manage_houses(request: Request, db: Session = Depends(get_db), account: Users = Depends(get_current_user_from_token)):
    if not account.is_superuser:
        raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted."))
    houses = list_false_houses(db=db)
    return templates.TemplateResponse("houses/manage-houses.html",
                                      {"request": request, "account": account, "houses": houses})


@router.put("/allow/{id}")
def allow_house(id: int, request: Request, db: Session = Depends(get_db), account: Users = Depends(get_current_user_from_token)):
    if not account.is_superuser:
        raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted."))
    try:
        active_house_by_id(id=id, db=db, current_user=account)
        return "Succeed."
    except:
        return "Failed, contact the owner."


@router.put("/disable/{id}")
def allow_house(id: int, request: Request, db: Session = Depends(get_db), account: Users = Depends(get_current_user_from_token)):
    if not account.is_superuser:
        raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted."))
    try:
        deactive_house_by_id(id=id, db=db, current_user=account)
        return "Succeed."
    except:
        return "Failed, contact the owner."
