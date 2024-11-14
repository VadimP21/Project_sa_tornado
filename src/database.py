"""
Файл с конфигурацией базы данных
"""

import os
from typing import Annotated

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column

load_dotenv()

"""
engine - синхронный движок
async_engine - асинхронный движок
"""
engine = create_engine(url=os.getenv("DB_POSTGRES_URL"))

async_engine = create_async_engine(url=os.getenv("DB_POSTGRES_URL"))

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

    type_annotation_map = {}
    pass
