from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.controllers import cart_controller

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

MOCK_CART = [
    {"id": 1, "name": "Laptop Gamer",        "price": 2500.00, "qty": 1, "stock": 5},
    {"id": 2, "name": "Mouse Inalámbrico",    "price": 120.00,  "qty": 2, "stock": 10},
    {"id": 3, "name": "Teclado Mecánico",     "price": 350.00,  "qty": 1, "stock": 12},
]

def _totals():
    subtotal = sum(item["price"] * item["qty"] for item in MOCK_CART)
    shipping = 0.0  # mock
    taxes = 0.0     # mock
    total = subtotal + shipping + taxes
    return {"subtotal": subtotal, "shipping": shipping, "taxes": taxes, "total": total}


@cart_bp.get("/")
def index():
    return render_template("cart/index.html", items=MOCK_CART, totals=_totals())

# 🔸 Acciones simuladas (no persisten)
@cart_bp.post("/<int:product_id>/remove")
def remove(product_id: int):
    flash("Acción simulada: no se ha removido realmente (mock).", "info")
    return redirect(url_for("cart.index"))

@cart_bp.post("/<int:product_id>/qty")
def update_qty(product_id: int):
    qty = request.form.get("qty", type=int, default=1)
    flash(f"Acción simulada: qty={qty} (mock, sin persistir).", "info")
    return redirect(url_for("cart.index"))

@cart_bp.post("/clear")
def clear():
    flash("Acción simulada: carrito no se limpia (mock).", "info")
    return redirect(url_for("cart.index"))

@cart_bp.post("/checkout")
def checkout():
    flash("Acción simulada: checkout (mock).", "success")
    return redirect(url_for("cart.index"))