from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from db.session import get_db
from typing import List
from schemes.house import CreateHouse, ShowHouse
from db.repository.house import create_new_house, retrieve_house, list_houses, update_house_by_id, delete_house_by_id
from apis.routes.route_login import get_current_user_from_token
from db.models.users import Users

router = APIRouter()


@router.post("/create", response_model=ShowHouse)
def create_house(given_house: CreateHouse, db: Session = Depends(get_db),
                 current_user: Users = Depends(get_current_user_from_token)):
    return create_new_house(given_house=given_house, db=db, owner_id=current_user.id)


@router.get("/get/{id}", response_model=ShowHouse)
def retrieve_house_by_id(id: int, db: Session = Depends(get_db)):
    house = retrieve_house(id=id, db=db)
    if not house:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} does not exist"))
    return house


@router.get('/get_all', response_model=List[ShowHouse])
def retrieve_all_houses(db: Session = Depends(get_db)):
    return list_houses(db=db)


@router.put("/update/{id}")
def update_house(id: int, house: CreateHouse, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    message = update_house_by_id(id=id, house=house, db=db, current_user=current_user)
    if not message:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} doesn't exist"))
    return {"detail": "Successfully updated the data."}


@router.delete("/delete/{id}")
def delete_house(id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    house = retrieve_house(id=id, db=db)
    if not house:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} doesn't exist"))
    if house.owner_id == current_user.id or current_user.is_superuser:
        if delete_house_by_id(id=id, db=db, owner_id=current_user.id):
            return {"detail": "House successfully deleted."}
        else:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} doesn't exist"))
    raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted."))


"""
@router.post("/upload/")
async def upload_house_image(images: List[UploadFile] = File(...)):
    for image in images:
        image_location = f"./static/images/{image.filename}"
        with open(image_location, "wb+") as file_object:
            file_object.write(image.file.read())
    return {"info":"The Images saved at '/static/images/'"}
"""
