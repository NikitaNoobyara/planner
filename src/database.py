from config import DB_USER, DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT
from sqlalchemy.ext.asyncio import create_async_engine
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine=create_async_engine(DATABASE_URL)