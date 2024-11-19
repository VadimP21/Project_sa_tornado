from unicodedata import category

from sqlalchemy.orm import joinedload

from database import session_factory


class ProductQueries:
    @staticmethod
    def last_version_product_by_name_query(
        session: session_factory, name: str, model: "ProductOrm"
    ):
        return (
            session.query(model)
            .filter_by(name=name)
            .options(joinedload(model.categories))
            .order_by(model.version.desc())
            .first()
        )

    @staticmethod
    def first_product_by_id_query(
        session: session_factory, product_id: int, model: "ProductOrm"
    ):
        return session.query(model).filter_by(id=int(product_id)).first()

    @staticmethod
    def products_versions_to_upgrade_query(
        session: session_factory, name: str, new_name: str, model: "ProductOrm"
    ):
        return session.query(model).filter_by(name=name).update({model.name: new_name})

    @staticmethod
    def products_by_name_archived_query(
        session: session_factory, name: str, model: "ProductOrm"
    ):
        return session.query(model).filter_by(name=name).update({model.archived: True})


class CategoriesQueries:
    @staticmethod
    def existing_category_by_name_query(
        session: session_factory, name: str, model: "CategoryOrm"
    ):
        return session.query(model).filter_by(name=name).first()

    @staticmethod
    def category_by_id_query(
        session: session_factory, category_id: int, model: "CategoryOrm"
    ):
        return session.get(model, category_id)

    @staticmethod
    def category_upgrade_query(
        session: session_factory,
        model: "CategoryOrm",
        category_id: str,
        new_name: str | None,
        new_description: str | None,
    ):
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
