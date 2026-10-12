from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

# Create database engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

local_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

BASE = declarative_base()


async def get_db():
    async with local_session() as db:
        yield db