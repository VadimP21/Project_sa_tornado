"""Модели DTO"""

from sqlalchemy import asc, desc, select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import InvalidRequestError

from db_repository.base import ProductQueries, CategoriesQueries
from models.models import ProductOrm, CategoryOrm, str255
from settings.database import session_factory, Base, engine


class AsyncOrm:
    pass


class ProductRepository:
    """
    Класс-репозиторий для работы с Product.
    Принимает объекты DTO, организует сессию в БД и возвращает модель БД.
    Обрабатывает исключения, связанные с БД
    """

    @staticmethod
    def last_version_product_by_name_repository(
        product_dto: "BaseModel",
    ) -> str | None:
        """
        Last version of Product by NAME
        Using in GET, POST
        """
        with session_factory() as session:
            result = session.execute(
                select(ProductOrm)
                # .where(ProductOrm.archived.in_([None, False,]))
                .filter_by(name=product_dto.name)
                .order_by(ProductOrm.version.desc())
                .limit(1)
            ).scalar_one_or_none()
        return result

    @staticmethod
    def get_product_by_id_repository(
        product_dto: "ProductSearchByIdDTO",
    ) -> str | None:
        """
        Last version of Product by ID
        Using in GET, UPDATE, DELETE
        """
        with session_factory() as session:
            try:
                result = session.execute(
                    select(ProductOrm).filter_by(id=product_dto.id)
                ).scalar_one_or_none()
            except Exception as e:
                session.rollback()
                print(f"Ошибка получения продукта: {e}")
        return result

    @staticmethod
    def create_new_version_of_existing_product(
        product_dto: "ProductPostDTO",
    ) -> ProductOrm | None:
        """
        Create a new version of existing Product
        Using in POST
        """
        try:
            with session_factory() as session:
                data = product_dto.model_dump()
                new_product_orm = ProductOrm(**data)
                session.add(new_product_orm)
                session.flush()
                session.commit()
                session.refresh(new_product_orm)
                return new_product_orm
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def create_product(product: "ProductPostDTO") -> "ProductOrm":
        """
        Добавляет в БД новый продукт.
        Используется в POST
        :param product: модель продукта DTO
        :return: "ProductOrm"
        """

        with session_factory() as session:
            data = product.model_dump()
            new_product_orm = ProductOrm(**data)
            session.add(new_product_orm)
            session.flush()
            session.commit()
            session.refresh(new_product_orm)
            return new_product_orm

    @staticmethod
    def update_last_version_of_existing_product_by_id_repository(
        product_to_update_dto: str, product_with_new_price_dto: str
    ) -> ProductOrm | None:
        """
        Create a new version of existing Product
        Using in PATCH
        """
        with session_factory() as session:
            product_to_update_data = product_to_update_dto.model_dump()
            product_with_new_price_data = product_with_new_price_dto.model_dump()

            product_to_update_orm = session.get(
                ProductOrm, product_to_update_data["id"]
            )
            product_to_update_orm.price = product_with_new_price_data["price"]
            session.flush()
            session.commit()
            session.refresh(product_to_update_orm)
        return product_to_update_orm

    @staticmethod
    def get_all_versions_of_products_by_name(
        product_to_archive_dto: str,
    ) -> list["ProductOrm"] | None:
        """
        Get all versions of existing Product
        Using in DELETE
        """
        with session_factory() as session:
            result = (
                session.execute(
                    select(ProductOrm).filter_by(name=product_to_archive_dto.name)
                )
                .scalars()
                .all()
            )
        return result

    @staticmethod
    def archive_all_product_in_list_by_name(
        product_to_archived_dto: "BaseModel",
    ) -> None:
        """
        Archive all versions od product by name
        Using in DELETE
        """

        with session_factory() as session:
            try:
                stmt = (
                    update(ProductOrm).where(
                        ProductOrm.name == product_to_archived_dto.name
                    )
                    # .where(ProductOrm.id.in_(product_ids))
                    .values(archived=True)
                )
                session.execute(stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Ошибка удаления продуктов: {e}")

    @staticmethod
    def archive_product_by_id_repository(
        product_to_archived_dto: "BaseModel",
    ) -> None:
        """
        Archive Product by ID
        Using in DELETE
        """
        with session_factory() as session:
            try:
                stmt = (
                    update(ProductOrm).where(
                        ProductOrm.id == product_to_archived_dto.id
                    )
                    # .where(ProductOrm.id.in_(product_ids))
                    .values(archived=True)
                )
                session.execute(stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Ошибка удаления продукта: {e}")


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
                    session=session, model=ProductOrm, name=name
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
    def get_product_list(
        page_number: str,
        page_size: str,
        sort_field: str,
        sort_order: str,
        product_version: str,
    ) -> dict[str : str255 | int]:
        """
        Получает продукты с заданной страницей, размером страницы, полем сортировки и направлением сортировки.

        :param page_number:
        :param page_size:
        :param sort_field:
        :param sort_order:
        :param product_version:
        :return:
        """
        with session_factory() as session:

            try:
                page_number = int(page_number)
                page_size = int(page_size)
            except ValueError:
                return {
                    "ValueError": "Неверные параметры страницы или размера страницы"
                }, 400
            try:
                if sort_order.lower() == "asc":
                    sort_direction = asc(
                        ProductOrm.__table__.c[sort_field]
                    )  # Ключевой момент!
                elif sort_order.lower() == "desc":
                    sort_direction = desc(
                        ProductOrm.__table__.c[sort_field]
                    )  # Ключевой момент!
                else:
                    return {"error": "Неверное направление сортировки"}, 400
            except KeyError:
                return {"error": f"Поле '{sort_field}' не найдено в таблице"}, 400
            except (AttributeError, InvalidRequestError) as e:
                return {"error": str(e)}, 400

            offset: int = (page_number - 1) * page_size
            limit: int = page_size

            if product_version == "last":
                products = ProductQueries.last_version_products_with_pagination_and_sort_by_field_query(
                    session=session,
                    model=ProductOrm,
                    sort_direction=sort_direction,
                    offset=offset,
                    limit=limit,
                )
            elif int(product_version):
                products = ProductQueries.all_specific_version_products_with_pagination_and_sort_by_field_query(
                    session=session,
                    model=ProductOrm,
                    sort_direction=sort_direction,
                    offset=offset,
                    limit=limit,
                    product_version=int(product_version),
                )
            else:
                return {
                    "ValueError": "Неверное указание версии продукта, укажите 'last' или номер в числовом виде"
                }, 400
            products_to_result = []
            for product in products:
                products_to_result.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "version": product.version,
                        # "created_at": product.created_at,
                        # "updated_at": product.updated_at,
                        "archived": product.archived,
                    }
                )
            result = {
                "products": products_to_result,
                "total_count": len(products_to_result),
            }

            return result

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
                session=session, model=ProductOrm, product_id=int(product_id)
            )
            last_name = first_product_by_name.name
            products_versions_to_upgrade = (
                product_query.products_versions_to_upgrade_query(
                    session=session,
                    model=ProductOrm,
                    name=last_name,
                    new_name=new_name,
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
                session=session, model=ProductOrm, name=name
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
                session=session, model=CategoryOrm, name=name
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
            category_to_upgrade = CategoriesQueries.category_by_id_query(
                session=session, model=CategoryOrm, category_id=category_id
            )
            last_name = category_to_upgrade.name
            last_description = category_to_upgrade.description
            CategoriesQueries.category_upgrade_query(
                session=session,
                model=CategoryOrm,
                category_id=category_id,
                new_name=new_name,
                new_description=new_description,
            )
            result = {
                "last_name": last_name,
                "new_name": category_to_upgrade.name,
                "last_description": last_description,
                "new_description": category_to_upgrade.description,
            }
            session.commit()
            return result

    @staticmethod
    def archive_category(category_id: str) -> dict[str : str255 | int]:
        """
        Удаляет все версии продукта по имени
        :param category_id: ID категории
        :return:
        """
        with session_factory() as session:
            category_query = CategoriesQueries()

            category_by_id_archived = category_query.category_by_id_archived_query(
                session=session, model=CategoryOrm, category_id=category_id
            )
            result = {
                "id": category_id,
                "amount_archived_products": category_by_id_archived,
            }
            session.commit()
            return result
