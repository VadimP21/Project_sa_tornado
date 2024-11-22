from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload
from database import session_factory


class ProductQueries:
    @staticmethod
    def all_specific_version_products_with_pagination_and_sort_by_field_query(
        session: session_factory,
        model: "ProductOrm",
        sort_direction: desc,
        offset: int,
        limit: int,
        product_version: int,
    ):
        """
        Возвращает
        :param session:
        :param model:
        :param sort_direction:
        :param offset:
        :param limit:
        :param product_version:
        :return:
        """
        return (
            session.query(model)
            .filter_by(version=product_version)
            .order_by(sort_direction)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def last_version_products_with_pagination_and_sort_by_field_query(
        session: session_factory,
        model: "ProductOrm",
        sort_direction: desc,
        offset: int,
        limit: int,
    ):
        subquery = (
            session.query(
                model.id, func.max(model.version).label("max_version")
            )
            .group_by(model.id)
            .subquery()
        )

        products = (
            session.query(model)
            .join(subquery, model.id == subquery.c.id)
            .filter(model.version == subquery.c.max_version)
            .order_by(sort_direction)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return products
    @staticmethod
    def last_version_product_by_name_query(
        session: session_factory, model: "ProductOrm", name: str
    ):
        """
        Возвращает последнюю версию продукта по имени
        :param session: Сессия обращения в БД
        :param model: ProductOrm
        :param name: Имя продукта
        :return: инстанс ProductOrm
        """
        return (
            session.query(model)
            .filter_by(name=name)
            .options(joinedload(model.categories))
            .order_by(model.version.desc())
            .first()
        )

    @staticmethod
    def first_product_by_id_query(
        session: session_factory, model: "ProductOrm", product_id: int
    ):
        """
        Возвращает первый продукт по ID
        :param session: Сессия обращения в БД
        :param model: ProductOrm
        :param product_id: ID продукта
        :return : инстанс ProductOrm
        """
        return session.query(model).filter_by(id=int(product_id)).first()

    @staticmethod
    def products_versions_to_upgrade_query(
        session: session_factory, model: "ProductOrm", name: str, new_name: str
    ):
        """
        Обновляет имя продукта по текущему имени
        :param session: Сессия обращения в БД
        :param model: ProductOrm
        :param name: имя продукта
        :param new_name: текущее имя продукта
        :return : инстанс ProductOrm
        """
        if name != new_name:
            return (
                session.query(model).filter_by(name=name).update({model.name: new_name})
            )
        else:
            return

    @staticmethod
    def products_by_name_archived_query(
        session: session_factory, model: "ProductOrm", name: str
    ):
        """
        Архивирует продукт по имени
        :param session: Сессия обращения в БД
        :param model: ProductOrm
        :param name: имя продукта
        :return : инстанс ProductOrm
        """
        return session.query(model).filter_by(name=name).update({model.archived: True})


class CategoriesQueries:
    @staticmethod
    def existing_category_by_name_query(
        session: session_factory, model: "CategoryOrm", name: str
    ):
        """
        Возвращает первую категорию по имени
        :param session: Сессия обращения в БД
        :param model: CategoryOrm
        :param name: имя категории
        :return : инстанс CategoryOrm
        """
        return session.query(model).filter_by(name=name).first()

    @staticmethod
    def category_by_id_query(
        session: session_factory, model: "CategoryOrm", category_id: str
    ):
        """
        Возвращает категорию по ID
        :param session: Сессия обращения в БД
        :param model: CategoryOrm
        :param category_id: ID категории
        :return : инстанс CategoryOrm
        """
        return session.get(model, int(category_id))

    @staticmethod
    def category_upgrade_query(
        session: session_factory,
        model: "CategoryOrm",
        category_id: str,
        new_name: str | None,
        new_description: str | None,
    ):
        """
        Обновляет категорию по ID
        :param session: Сессия обращения в БД
        :param model: CategoryOrm
        :param category_id: ID категории
        :param new_name: новое имя категории
        :param new_description: новое описание категории
        :return : инстанс CategoryOrm
        """
        if new_name and new_description:
            return (
                session.query(model)
                .filter_by(id=int(category_id))
                .update({model.name: new_name, model.description: new_description})
            )
        elif new_name:
            return (
                session.query(model)
                .filter_by(id=int(category_id))
                .update({model.name: new_name})
            )
        elif new_description:
            return (
                session.query(model)
                .filter_by(id=int(category_id))
                .update({model.description: new_description})
            )
        else:
            return

    @staticmethod
    def category_by_id_archived_query(
        session: session_factory, model: "CategoryOrm", category_id: str
    ):
        """
        Архивирует категорию по ID
        :param session: Сессия обращения в БД
        :param model: CategoryOrm
        :param category_id: ID продукта
        :return : инстанс CategoryOrm
        """
        return (
            session.query(model)
            .filter_by(id=int(category_id))
            .update({model.archived: True})
        )
