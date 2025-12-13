from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, sweets

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sweet Shop Management System")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(sweets.router, prefix="/api/sweets", tags=["Sweets"])
