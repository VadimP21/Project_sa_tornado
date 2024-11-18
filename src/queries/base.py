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
    def first_product_by_name_query(
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
