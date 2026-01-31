from fastapi import FastAPI
from routes import jwt, customer, manager
from db.base import Base
from db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banking System")

app.include_router(jwt.router)
app.include_router(manager.router)
app.include_router(customer.router)
