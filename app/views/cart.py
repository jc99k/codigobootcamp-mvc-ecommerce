from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.controllers.cart_controller import CartController

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route('/')
@login_required
def index():
    cart_items = CartController.get_cart_items()
    totals = CartController.calculate_cart_totals()
    return render_template('cart/index.html', items=cart_items, totals=totals)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    success, message = CartController.add_to_cart(product_id, quantity)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for("product.detail", product_id=product_id))


@cart_bp.route("/empty", methods=["POST"])
@login_required
def empty_cart():
    CartController.empty_cart(current_user.id)
    return redirect(url_for("cart.index"))


@cart_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    success, message = CartController.update_quantity(product_id, quantity)
    flash(message, "success" if success else "error")
    return redirect(url_for("cart.index"))


@cart_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    success, message = CartController.remove_item(product_id)
    flash(message, "success" if success else "error")
    return redirect(url_for("cart.index"))


# 🔸 Acciones simuladas (no persisten)
@cart_bp.post("/checkout")
def checkout():
    flash("Acción simulada: Checkout (mock).", "success")
    return redirect(url_for("cart.index"))


