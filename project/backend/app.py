from fastapi import FastAPI
from database import Base, engine
from routes import users, equipment, borrow

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Equipment Management System")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(equipment.router, prefix="/equipment", tags=["Equipment"])
app.include_router(borrow.router, prefix="/borrow", tags=["Borrow"])