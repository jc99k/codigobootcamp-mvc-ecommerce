from flask import Blueprint, render_template, request
from app.controllers import product_controller

product_bp = Blueprint("product", __name__, url_prefix="/products")

MOCK_PRODUCTS = [
    {"id": 1, "name": "Laptop Gamer", "price": 2500.00, "stock": 10},
    {"id": 2, "name": "Mouse Inalámbrico", "price": 120.00, "stock": 50},
    {"id": 3, "name": "Teclado Mecánico", "price": 350.00, "stock": 30},
    {"id": 4, "name": "Monitor 4K", "price": 1500.00, "stock": 0},
]

@product_bp.get("/")
def index():
    # page = int(request.args.get("page", 1))
    # products = product_controller.list_products(page=page, per_page=12)
    products=MOCK_PRODUCTS
    return render_template("products/index.html", products=products)

@product_bp.get("/<int:product_id>")
def detail(product_id: int):
    # product = product_controller.get_product(product_id)
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    return render_template("products/detail.html", product=product), (200 if product else 404)
