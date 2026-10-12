# from fastapi import FastAPI

# import app.model.user
# import app.model.expense

# from app.core.db import BASE, engine

# app = FastAPI()

# BASE.metadata.create_all(bind=engine)


# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Expense Tracker API"}
from app.routers.expense import expense_router
from app.routers.user import user_router
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from app.routers.auth import auth_router
import app.model.user
import app.model.expense

from app.core.db import BASE, engine

app = FastAPI()
app.include_router(expense_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker API"}