from flask import Blueprint, render_template, request
from app.controllers.product_controller import ProductController

product_bp = Blueprint("product", __name__, url_prefix="/products")


@product_bp.get("/")
def index():
    page = int(request.args.get("page", 1))
    products = ProductController.get_all_products(page=page, per_page=12)
    return render_template("products/index.html", products=products)


@product_bp.get("/<int:product_id>")
def detail(product_id: int):
    product = ProductController.get_product_by_id(product_id)
    return render_template("products/detail.html", product=product), (200 if product else 404)
