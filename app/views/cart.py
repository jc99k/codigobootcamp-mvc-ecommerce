from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.cart_controller import CartController
from flask_login import login_required

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
@login_required
def index():
    cart_items = CartController.get_cart_items()
    total = CartController.calculate_cart_total()
    return render_template('cart/index.html', cart_items=cart_items, total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    success, message = CartController.add_to_cart(product_id, quantity)

    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')

    return redirect(request.referrer or url_for('product.index'))


@cart_bp.route('/cart/items/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    """
    Actualiza la cantidad de un item en el carrito
    """
    new_quantity = request.json.get('quantity', 1)
    
    success, message = CartController.update_cart_item_quantity(item_id, new_quantity)
    
    if success:
        return {'success': True, 'message': message}, 200
    else:
        return {'success': False, 'message': message}, 400