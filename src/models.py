"""
Модели БД
"""

import datetime
from typing import Annotated

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str255 = Annotated[str, 255]


class Product(Base):
    __tablename__ = "product"
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

    categories: Mapped[list["Category"]] = relationship(
        secondary="category_product_m2m",
        back_populates="categories"
    )

class Category(Base):
    __tablename__ = "category"
    id: Mapped[pk]
    name: Mapped[str255]
    description: Mapped[str255]

    products: Mapped[list["Product"]] = relationship(
        secondary="category_product_m2m",
        back_populates="products"
    )

class CategoryProductM2M(Base):
    __tablename__ = "category_product_m2m"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"),
        primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        primary_key=True
    )
