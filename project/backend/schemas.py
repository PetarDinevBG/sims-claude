from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    password: str
    role: str

    class Config:
        orm_mode = True
      
class RoleUpdate(BaseModel):
    role: str
      
class ItemCreate(BaseModel):
    name: str
    type: str
    serial_number: str
    condition: str
    status: str
    location: str
  

class ItemOut(BaseModel):
    id: int
    name: str
    type: str
    serial_number: Optional[str]
    condition: Optional[str]
    status: Optional[str]
    location: Optional[str]

    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    username: str
    password: str