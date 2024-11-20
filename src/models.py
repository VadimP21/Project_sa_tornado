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


class ProductOrm(Base):
    __tablename__ = "product"
    id: Mapped[pk]
    name: Mapped[str255]
    version: Mapped[int] = mapped_column(default=1)
    price: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"), onupdate=datetime.datetime.utcnow
    )
    archived: Mapped[bool] = mapped_column(nullable=True)

    categories: Mapped[list["CategoryOrm"]] = relationship(
        secondary="category_product_m2m", back_populates="products"
    )


class CategoryOrm(Base):
    __tablename__ = "category"
    id: Mapped[pk]
    name: Mapped[str255]
    description: Mapped[str255 | None]
    archived: Mapped[bool] = mapped_column(nullable=True)

    products: Mapped[list["ProductOrm"]] = relationship(
        secondary="category_product_m2m", back_populates="categories"
    )


class CategoryProductM2MOrm(Base):
    __tablename__ = "category_product_m2m"

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), primary_key=True
    )
