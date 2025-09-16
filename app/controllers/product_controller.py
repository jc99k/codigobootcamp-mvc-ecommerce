from app.models.product import Product
from app import db


class ProductController:
    @staticmethod
    def get_all_products(page=1, per_page=12):
        return Product.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get_or_404(product_id)

    # @staticmethod
    # def get_products_by_category(category_id):
    #     return Product.query.filter_by(category_id=category_id).all()

    @staticmethod
    def search_products(query):
        return Product.query.filter(
            Product.name.contains(query) |
            Product.description.contains(query)
        ).all()