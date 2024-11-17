from sqlalchemy import select, func, cast, Integer, and_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from sqlalchemy.sql.operators import contains
from tornado import version
from src.models import ProductOrm, CategoryOrm
from database import session_factory, async_session_factory, Base, engine


class AsyncOrm:
    pass


class SyncORM:
    @staticmethod
    def create_tables():
        engine.echo = False
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_products_and_categories():
        """
        Добавляет 5 продуктов и 3 категории
        """
        with session_factory() as session:
            products_to_add = [
                {"name": "Phone", "price": 5000},
                {"name": "Laptop", "price": 10000},
                {"name": "Notebook", "price": 50000},
                {"name": "Stove", "price": 20000},
                {"name": "Fridge", "price": 60000},
            ]
            categories_to_add = [
                {"name": "Household appliances"},
                {"name": "Digital technology"},
                {"name": "Discount"},
            ]
            insert_products = insert(ProductOrm).values(products_to_add)
            insert_categories = insert(CategoryOrm).values(categories_to_add)
            session.execute(insert_products)
            session.execute(insert_categories)
            session.flush()
            prod_1 = session.get(ProductOrm, 1)
            prod_2 = session.get(ProductOrm, 2)
            prod_3 = session.get(ProductOrm, 3)
            prod_4 = session.get(ProductOrm, 4)
            prod_5 = session.get(ProductOrm, 5)
            category_1 = session.get(CategoryOrm, 1)
            category_2 = session.get(CategoryOrm, 2)
            category_3 = session.get(CategoryOrm, 3)
            category_1.products.append(prod_4)
            category_1.products.append(prod_5)
            category_2.products.append(prod_1)
            category_2.products.append(prod_2)
            category_2.products.append(prod_3)
            category_3.products.append(prod_2)
            category_3.products.append(prod_3)
            category_3.products.append(prod_4)
            session.commit()

    @staticmethod
    def create_product(name: str, price: int) -> dict[str:str | int]:
        """
        Добавляет в БД новый продукт или новую версию существующего
        :param name: имя продукта
        :param price: стоимость продукта
        :return: dict
        """
        with session_factory() as session:
            last_version_product_by_name = (
                session.query(ProductOrm)
                .filter_by(name=name)
                .options(joinedload(ProductOrm.categories))
                .order_by(ProductOrm.version.desc())
                .first()
            )
            if last_version_product_by_name:
                next_version = last_version_product_by_name.version + 1
                new_product = ProductOrm(name=name, price=price, version=next_version)
                existing_product_categories: list = (
                    last_version_product_by_name.categories
                )
                new_product.categories.extend(existing_product_categories)
                already_existing = 1
            else:
                new_product = ProductOrm(name=name, price=price)
                already_existing = 0
            session.add(new_product)
            new_product_params = {
                "already_existing": already_existing,
                "id": new_product.id,
                "name": new_product.name,
                "price": new_product.price,
                "version": new_product.version,
            }
            session.commit()
            return new_product_params

    @staticmethod
    def create_category(name: str, description: str | None) -> dict[str:str | int]:
        """
        Добавляет в БД новый продукт или новую версию существующего
        :param name: имя категории
        :param description: описание категории
        :return: dict
        """
        with session_factory() as session:
            existing_category_by_name = (
                session.query(CategoryOrm)
                .filter_by(name=name)
                .first()
            )
            print(existing_category_by_name)
            if existing_category_by_name:
                new_category_params = {
                    "already_existing": 1,
                    "id": existing_category_by_name.id,
                    "name": existing_category_by_name.name,
                    "description": existing_category_by_name.description,
                }
            else:
                new_category = CategoryOrm(name=name, description=description)
                new_category_params = {
                    "already_existing": 0,
                    "id": new_category.id,
                    "name": new_category.name,
                    "description": new_category.description,
                }
            session.commit()
            return new_category_params
