from app.core.db import BASE
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float,Date,ForeignKey,Boolean

class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime,nullable=False, default=datetime.utcnow)