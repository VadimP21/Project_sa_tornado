"""
Модели БД
"""
import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str255 = Annotated[str, 255]


class Product(Base):
    id: Mapped[pk]
    name: Mapped[str255]
    version: Mapped[int] = mapped_column(default=0)
    price: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"), onupdate=datetime.datetime.utcnow
    )


class Category(Base):
    id: Mapped[pk]
    name: Mapped[str255]
    description: Mapped[str255]
