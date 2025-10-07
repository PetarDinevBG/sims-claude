from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, auth, schemas

router = APIRouter()
db: Session = database.SessionLocal()

@router.post("/register")
def register(user: schemas.UserCreate):
    hashed = auth.hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created", "user": db_user.username}

@router.post("/login")
def login(user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username==user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}