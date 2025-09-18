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

<<<<<<< HEAD
        # Debug: imprimir información
        print(f"DEBUG: Adding product_id={product_id}, quantity={quantity}, user_id={current_user.id}")
=======
        product = Product.query.get(product_id)
        if not product or product.stock < quantity:
            return False, "Producto con stock insuficiente."
>>>>>>> main

        product = Product.query.get(product_id)
        if not product:
            print(f"DEBUG: Product with id {product_id} not found")
            return False, "Product not found"
        
        print(f"DEBUG: Found product: {product.name} (ID: {product.id})")
        
        if product.stock < quantity:
            return False, f"Only {product.stock} items available"

        # Buscar si ya existe un item en el carrito para este producto
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if cart_item:
            # Si ya existe, verificar que no exceda el stock total
            new_total_quantity = cart_item.quantity + quantity
            if new_total_quantity > product.stock:
                return False, f"Only {product.stock} items available (you already have {cart_item.quantity})"
            
            # Actualizar cantidad existente
            cart_item.quantity = new_total_quantity
            message = f"Quantity updated to {new_total_quantity} for {product.name}"
        else:
            # Crear nuevo item en el carrito
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            message = f"Added {product.name} to cart successfully"
            print(f"DEBUG: Created new cart item for product {product.name} (ID: {product_id})")

        db.session.commit()
<<<<<<< HEAD
        return True, message
=======
        return True, "Producto agregado al carrito."
>>>>>>> main

    @staticmethod
    def get_cart_items():
        if not current_user.is_authenticated:
            return []

        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        # Debug: imprimir información de los items del carrito
        print(f"DEBUG: Found {len(cart_items)} cart items for user {current_user.id}")
        for item in cart_items:
            print(f"DEBUG: Cart item - ID: {item.id}, Product ID: {item.product_id}, Quantity: {item.quantity}")
            if item.product:
                print(f"DEBUG: Product name: {item.product.name}")
            else:
                print(f"DEBUG: Product with ID {item.product_id} not found!")
        
        return cart_items

    @staticmethod
    def calculate_cart_totals():
        cart_items = CartController.get_cart_items()
<<<<<<< HEAD
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

    @staticmethod
    def get_cart_debug_info():
        """
        Método para debuggear - muestra información detallada del carrito
        """
        if not current_user.is_authenticated:
            return "User not authenticated"
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        debug_info = f"User ID: {current_user.id}\n"
        debug_info += f"Total cart items: {len(cart_items)}\n"
        
        for item in cart_items:
            debug_info += f"- Item ID: {item.id}, Product ID: {item.product_id}, Quantity: {item.quantity}\n"
        
        return debug_info

    @staticmethod
    def clear_cart():
        """
        Vacía completamente el carrito del usuario actual
        """
        if not current_user.is_authenticated:
            return False, "User must be logged in"
        
        # Obtener todos los items del carrito del usuario
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            return False, "Cart is already empty"
        
        # Eliminar todos los items del carrito
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        return True, f"Cart cleared successfully. Removed {len(cart_items)} items."
=======
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
>>>>>>> main
