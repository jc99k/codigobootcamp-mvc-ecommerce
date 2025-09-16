from flask import Blueprint, render_template, request
from app.controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
@product_bp.route('/products')
def index():
    page = request.args.get('page', 1, type=int)
    products = ProductController.get_all_products(page)
    return render_template('products/index.html', products=products)

@product_bp.route('/products/<int:product_id>')
def detail(product_id):
    product = ProductController.get_product_by_id(product_id)
    return render_template('products/detail.html', product=product)

@product_bp.route('/search')
def search():
    query = request.args.get('q', '')
    products = ProductController.search_products(query) if query else []
    return render_template('products/index.html', products=products, query=query)