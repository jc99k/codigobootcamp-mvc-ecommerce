from app.models.cart import CartItem
from app.models.product import Product
from app import db
from flask_login import current_user


class CartController:
    @staticmethod
    def add_to_cart(product_id, quantity=1):
        if not current_user.is_authenticated:
            return False, "Please log in to add items to cart"

        product = Product.query.get(product_id)
        if not product or product.stock < quantity:
            return False, "Product not available or insufficient stock"

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
        return True, "Item added to cart successfully"

    @staticmethod
    def get_cart_items():
        if not current_user.is_authenticated:
            return []

        return CartItem.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def calculate_cart_total():
        cart_items = CartController.get_cart_items()
        total = sum(item.product.price * item.quantity for item in cart_items)
        return total