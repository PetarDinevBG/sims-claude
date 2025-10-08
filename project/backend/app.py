from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal 
from models import User, Base
from schemas import UserCreate, UserOut
from database import engine, get_db


engine = create_engine("postgresql://myuser:mypassword@localhost/mydb")

app = FastAPI(title="Equipment Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists or error occurred.")
    return db_user

@app.get("/")
def read_root():
    return "Test response"

@app.get("/users/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(equipment.router, prefix="/equipment", tags=["Equipment"])
# app.include_router(borrow.router, prefix="/borrow", tags=["Borrow"])