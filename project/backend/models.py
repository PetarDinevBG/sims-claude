from sqlalchemy import Column, Integer, String
from database import Base
import enum

class StatusOptions(enum.Enum):
    available = "Available"
    checked_out = "Checked Out"
    under_repair = "Under Repair"
    retired = "Retired"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    type = Column(String,  index=True, nullable=True)
    serial_number = Column(String, default="0000",  index=True, nullable=True)
    condition = Column(String, default="New",  index=True, nullable=True)
    status = Column(String, default="Available",  index=True, nullable=True)
    location = Column(String, default="School",  index=True, nullable=True)
    photo_url = Column(String,default="/",  index=True, nullable=True)