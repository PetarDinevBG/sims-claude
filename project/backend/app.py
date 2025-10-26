from fastapi import FastAPI, Depends, HTTPException
import json
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal 
from models import User, Base, Item, Request, StatusOptions, RequestStatus
from auth import create_access_token
from schemas import UserCreate, UserOut, ItemCreate, ItemOut, UserLogin,UserRegister, RoleUpdate, RequestCreate, RequestOut
from database import engine, get_db


def create_default_admin():
    db: Session = SessionLocal()
    try:
        admin_user = db.query(User).filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password="admin",
                role="admin"  # multiple roles
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()
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
@app.on_event("startup")
def on_startup():
    create_default_admin()
    
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=user.password)
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
    return "Test response123"

@app.get("/users/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/items/", response_model=list[ItemOut])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@app.post("/items/", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, type=item.type)
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists or error occurred.")
    return db_item

@app.post("/login/")
def login(user:UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role, "user_id": user.id})
    return {"access_token": access_token}

@app.post("/register/", response_model=UserOut)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=user.password, role="user")
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists or error occurred.")
    return db_user

@app.patch("/users/{user_id}/role", response_model=UserOut)
def update_user_role(user_id: int, payload: RoleUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.role = payload.role
    try:
        db.commit()
        db.refresh(db_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update role")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(db_user)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete user")
    return {"detail": "User deleted"}

@app.delete("/items/{item_id}/")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        db.delete(db_item)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete item")
    return {"detail": "Item deleted"}
@app.patch("/items/{item_id}/", response_model=ItemOut)
def update_item(item_id: int, payload: dict, db: Session = Depends(get_db)):
    """
    Patch/update an item. Accepts a JSON object with any of the editable fields:
    name, type, serial_number, location, condition, status.
    Only provided fields will be updated.
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    allowed = {"name", "type", "serial_number", "location", "condition", "status"}
    changed = False
    for key, value in payload.items():
        if key in allowed:
            setattr(db_item, key, value)
            changed = True

    if not changed:
        raise HTTPException(status_code=400, detail="No updatable fields provided")

    try:
        db.commit()
        db.refresh(db_item)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update item")
    return db_item

@app.get("/requests/", response_model=list[RequestOut])
def get_requests(db: Session = Depends(get_db)):
    return db.query(Request).all()

@app.post("/requests/", response_model=RequestOut)
def create_request(req: RequestCreate, db: Session = Depends(get_db)):
    db_req = Request(
        user_id=getattr(req, "user_id", None),
        item_id=getattr(req, "item_id", None),
        status=getattr(req, "status", "pending"),
        # add other fields as your Request model defines them
    )
    if getattr(db_req, "status", None) == "approved":
        item = db.query(Item).filter(Item.id == db_req.item_id).first()
        if item:
            item.status = StatusOptions.checked_out.value
    db.add(db_req)
    try:
        db.commit()
        db.refresh(db_req)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create request")
    return db_req

@app.get("/requests/{request_id}/", response_model=RequestOut)
def get_request(request_id: int, db: Session = Depends(get_db)):
    db_req = db.query(Request).filter(Request.id == request_id).first()
    if not db_req:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_req

@app.patch("/requests/{request_id}/", response_model=RequestOut)
def update_request(request_id: int, payload: dict, db: Session = Depends(get_db)):
    db_req = db.query(Request).filter(Request.id == request_id).first()
    if not db_req:
        raise HTTPException(status_code=404, detail="Request not found")

    allowed = {"requester", "item_id", "status", "notes"}
    changed = False
    for key, value in payload.items():
        if key in allowed:
            setattr(db_req, key, value)
            changed = True

    if not changed:
        raise HTTPException(status_code=400, detail="No updatable fields provided")

    try:
        db.commit()
        db.refresh(db_req)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update request")
    return db_req

@app.delete("/requests/{request_id}/")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    db_req = db.query(Request).filter(Request.id == request_id).first()
    if not db_req:
        raise HTTPException(status_code=404, detail="Request not found")
    try:
        db.delete(db_req)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete request")
    return {"detail": "Request deleted"}