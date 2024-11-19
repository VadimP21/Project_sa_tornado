from sqlalchemy.dialects.mysql import insert

from queries.base import ProductQueries, CategoriesQueries
from src.models import ProductOrm, CategoryOrm, str255
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
    def create_product(name: str255, price: int) -> dict[str : str | int | bool]:
        """
        Добавляет в БД новый продукт или новую версию существующего
        :param name: имя продукта
        :param price: стоимость продукта
        :return: dict
        """
        with session_factory() as session:
            product_query = ProductQueries()
            last_version_product_by_name = (
                product_query.last_version_product_by_name_query(
                    session=session, name=name, model=ProductOrm
                )
            )
            if last_version_product_by_name:
                next_version = last_version_product_by_name.version + 1
                new_product = ProductOrm(name=name, price=price, version=next_version)
                existing_product_categories: list = (
                    last_version_product_by_name.categories
                )
                new_product.categories.extend(existing_product_categories)
                already_existing = True
            else:
                new_product = ProductOrm(name=name, price=price)
                already_existing = False
            session.add(new_product)
            session.flush()
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
    def upgrade_product(product_id: str, new_name: str255) -> dict[str : str255 | int]:
        """
        Обновляет все версии продукта по ID
        :param product_id: ID продукта
        :param new_name: Новое имя продукта
        :return: result
        """
        with session_factory() as session:
            product_query = ProductQueries()

            first_product_by_name = product_query.first_product_by_id_query(
                session=session, product_id=int(product_id), model=ProductOrm
            )
            last_name = first_product_by_name.name
            products_versions_to_upgrade = (
                product_query.products_versions_to_upgrade_query(
                    session=session,
                    name=last_name,
                    new_name=new_name,
                    model=ProductOrm,
                )
            )
            result = {
                "last_name": last_name,
                "new_name": new_name,
                "amount_upgraded_products": products_versions_to_upgrade,
            }
            session.commit()
            return result

    @staticmethod
    def archive_product(name: str255) -> dict[str : str255 | int]:
        """
        Удаляет все версии продукта по имени
        :param name: Имя продукта
        :return:
        """
        with session_factory() as session:
            product_query = ProductQueries()

            products_by_name_archived = product_query.products_by_name_archived_query(
                session=session, name=name, model=ProductOrm
            )
            result = {
                "name": name,
                "amount_archived_products": products_by_name_archived,
            }
            session.commit()
            return result

    @staticmethod
    def create_category(
        name: str255, description: str | None
    ) -> dict[str : str255 | int]:
        """
        Добавляет в БД новый продукт или новую версию существующего
        :param name: имя категории
        :param description: описание категории
        :return: dict
        """
        with session_factory() as session:
            category_query = CategoriesQueries()
            existing_category_by_name = category_query.existing_category_by_name_query(
                session=session, name=name, model=CategoryOrm
            )
            if existing_category_by_name:
                new_category_params = {
                    "already_existing": 1,
                    "id": existing_category_by_name.id,
                    "name": existing_category_by_name.name,
                    "description": existing_category_by_name.description,
                }
            else:
                new_category = CategoryOrm(name=name, description=description)
                session.add(new_category)
                session.flush()
                new_category_params = {
                    "already_existing": 0,
                    "id": new_category.id,
                    "name": new_category.name,
                    "description": new_category.description,
                }
                session.commit()
            return new_category_params

    @staticmethod
    def update_category(
        category_id: str, new_name: str255 | None, new_description: str | None
    ) -> dict[str : str255 | int]:
        """
        Обновляет данные категории продуктов по ID
        :param category_id: ID категории
        :param new_name: Новое имя категории
        :param new_description: Новое описание категории
        :return: result
        """

        with session_factory() as session:
            CategoriesQueries.category_upgrade_query(
                session=session,
                model=CategoryOrm,
                category_id=category_id,
                new_name=new_name,
                new_description=new_description,
            )
