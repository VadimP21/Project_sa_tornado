"""Модели DTO"""

from sqlalchemy import select, update
from models.models import ProductOrm
from settings.database import session_factory


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
