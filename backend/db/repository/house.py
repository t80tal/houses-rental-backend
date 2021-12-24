from sqlalchemy.orm import Session
from schemes.house import CreateHouse
from db.models.houses import Houses
from db.models.users import Users
from fastapi import HTTPException, status


def create_new_house(given_house: CreateHouse, db: Session, owner_id: int):
    house = Houses(**given_house.dict(), owner_id=owner_id)
    db.add(house)
    db.commit()
    db.refresh(house)
    return house


def retrieve_house(id: int, db: Session):
    return db.query(Houses).filter(Houses.id == id).first()


def list_houses(db: Session):
    return db.query(Houses).filter(Houses.is_active == True).all()


def update_house_by_id(id: int, house: CreateHouse, db: Session, current_user: Users):
    existing_house = db.query(Houses).filter(Houses.id == id)
    if not existing_house.first():
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} does not exist"))
    if existing_house.first().owner_id == current_user.id or current_user.is_superuser:
        house.__dict__["is_active"] = False
        if current_user.is_superuser:
            house.__dict__["is_active"] = True
        existing_house.update(house.__dict__)
        db.commit()
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Permitted", )


def delete_house_by_id(id: int, db: Session, owner_id: int):
    existing_house = db.query(Houses).filter(Houses.id == id)
    if not existing_house.first():
        return False
    existing_house.delete(synchronize_session=False)
    db.commit()
    return True


def get_houses_by_owner_id(id: int, db: Session):
    return db.query(Houses).filter(Houses.owner_id == id).all()


def list_false_houses(db: Session):
    return db.query(Houses).filter(Houses.is_active == False).all()


def active_house_by_id(id: int, db: Session, current_user: Users):
    if current_user.is_superuser:
        existing_house = db.query(Houses).filter(Houses.id == id)
        if not existing_house.first():
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} does not exist"))
        existing_house.update({"is_active": True})
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Permitted", )


def deactive_house_by_id(id: int, db: Session, current_user: Users):
    if current_user.is_superuser:
        existing_house = db.query(Houses).filter(Houses.id == id)
        if not existing_house.first():
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"House with id {id} does not exist"))
        existing_house.update({"is_active": False})
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Permitted", )
