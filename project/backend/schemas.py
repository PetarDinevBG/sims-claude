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
        
class ItemCreate(BaseModel):
    name: str
    type: str

class ItemOut(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    username: str
    password: str