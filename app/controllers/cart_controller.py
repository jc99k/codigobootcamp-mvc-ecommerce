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

    @staticmethod
    def update_cart_item_quantity(cart_item_id, new_quantity):
        """
        Actualiza la cantidad de un item en el carrito
        """
        # Validar que el usuario esté logueado
        if not current_user.is_authenticated:
            return False, "User must be logged in"
        
        # Buscar el item en el carrito
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return False, "Cart item not found"
        
        # Verificar que el item pertenece al usuario actual
        if cart_item.user_id != current_user.id:
            return False, "Unauthorized access"
        
        # Validar cantidad
        if new_quantity <= 0:
            return False, "Quantity must be greater than 0"
        
        # Verificar stock disponible
        if new_quantity > cart_item.product.stock:
            return False, f"Only {cart_item.product.stock} items available"
        
        # Actualizar cantidad
        cart_item.quantity = new_quantity
        db.session.commit()
        
        return True, "Quantity updated successfully"

    @staticmethod
    def increment_cart_item_quantity(cart_item_id):
        """
        Incrementa la cantidad de un item en el carrito en +1
        """
        # Validar que el usuario esté logueado
        if not current_user.is_authenticated:
            return False, "User must be logged in"
        
        # Buscar el item en el carrito
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return False, "Cart item not found"
        
        # Verificar que el item pertenece al usuario actual
        if cart_item.user_id != current_user.id:
            return False, "Unauthorized access"
        
        # Verificar stock disponible para incrementar
        if cart_item.quantity >= cart_item.product.stock:
            return False, f"Only {cart_item.product.stock} items available"
        
        # Incrementar cantidad en 1
        cart_item.quantity += 1
        db.session.commit()
        
        return True, "Quantity incremented successfully"