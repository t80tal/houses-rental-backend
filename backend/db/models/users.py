from db.base_class import Base
from sqlalchemy import Boolean, String, Column, Integer, Date
from sqlalchemy.orm import relationship


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    date_created = Column(Date)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    houses = relationship("Houses", back_populates="owner")

