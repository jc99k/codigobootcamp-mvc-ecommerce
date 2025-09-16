from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.controllers.cart_controller import CartController
from app import db
from flask_login import current_user
from datetime import datetime


class OrderController:
    @staticmethod
    def create_order():
        if not current_user.is_authenticated:
            return False, "Please log in to create an order"

        cart_items = CartController.get_cart_items()
        if not cart_items:
            return False, "Cart is empty"

        total_amount = CartController.calculate_cart_total()

        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount
        )
        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)

        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()

        db.session.commit()
        return True, f"Order #{order.id} created successfully"

    @staticmethod
    def get_user_orders():
        if not current_user.is_authenticated:
            return []

        return Order.query.filter_by(user_id=current_user.id).order_by(
            Order.created_at.desc()
        ).all()