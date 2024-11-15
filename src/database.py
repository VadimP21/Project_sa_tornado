"""
Файл с конфигурацией базы данных
"""

from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
"postgresql+psycopg://postgres:111@localhost/test_db"
db_url = f"{getenv('DB_ENGINE')}://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"
"""
engine - синхронный движок
async_engine - асинхронный движок
"""
engine = create_engine(url=db_url)

async_engine = create_async_engine(url=db_url)

"""
session_factory - синхронный создатель сеанса работы с БД
async_session_factory - асинхронный создатель сеанса работы с БД
"""
session_factory = sessionmaker(bind=engine)
async_session_factory = async_sessionmaker(bind=async_engine)


class Base(DeclarativeBase):
    """
    Base - родительский класс для моделей БД в декларативном виде
    """

    pass
