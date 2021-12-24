from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base


class Houses(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    address = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String)
    date_post = Column(Date)
    is_active = Column(Boolean(), default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="houses")
