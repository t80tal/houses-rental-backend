from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class HouseBase(BaseModel):
    title: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    date_post: Optional[date] = datetime.now().date()

class CreateHouse(HouseBase):
    title: str
    address: str
    price: int
    description: str

class ShowHouse(HouseBase):
    title: str
    address: str
    price: int
    description: str
    class Config():
        orm_mode = True