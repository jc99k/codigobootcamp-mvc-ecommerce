from app.models.cart import CartItem
from app.models.product import Product
from app import db
from flask_login import current_user
from decimal import Decimal


class CartController:
    @staticmethod
    def add_to_cart(product_id, quantity=1):
        if not current_user.is_authenticated:
            return False, "Inicie sesión para añadir productos al carrito."

        product = Product.query.get(product_id)
        if not product or product.stock < quantity:
            return False, "Producto con stock insuficiente."

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()
        return True, "Producto agregado al carrito."

    @staticmethod
    def get_cart_items():
        if not current_user.is_authenticated:
            return []

        return CartItem.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def calculate_cart_totals():
        cart_items = CartController.get_cart_items()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping = Decimal(0.0)  # mock
        taxes = Decimal(0.0)  # mock
        total = subtotal + shipping + taxes
        return {"subtotal": subtotal, "shipping": shipping, "taxes": taxes, "total": total}

    @staticmethod
    def empty_cart(user_id: int):
        """Remove all items from the user's cart"""
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    @staticmethod
    def update_quantity(product_id, quantity):
        """Update the quantity of a cart item"""
        if not current_user.is_authenticated:
            return False, "Inicie sesion para actualizar carrito"

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if not cart_item:
            return False, "Producto no encontrado en carrito"

        if quantity <= 0:
            # if quantity is 0 or negative, remove the item
            db.session.delete(cart_item)
            db.session.commit()
            return True, "Producto eliminado del carrito."

        cart_item.quantity = quantity
        db.session.commit()
        return True, "Carrito actualizado con éxito."

    @staticmethod
    def remove_item(product_id):
        """Remove a product completely from the cart"""
        if not current_user.is_authenticated:
            return False, "Inicie sesion para actualizar carrito"

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if not cart_item:
            return False, "Producto no encontrado en el carrito."

        db.session.delete(cart_item)
        db.session.commit()
        return True, "Producto eliminado del carrito."
