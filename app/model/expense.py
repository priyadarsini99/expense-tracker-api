from app.core.db import BASE
from .user import User
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float,Date,ForeignKey,Boolean

class Expense(BASE):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String(500), nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, default=datetime.utcnow)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    