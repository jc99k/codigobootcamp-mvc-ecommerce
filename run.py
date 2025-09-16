# File: run.py (Updated version)
from app import create_app, db
import os

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models.user import User
    from app.models.product import Product
    from app.models.cart import CartItem
    from app.models.order import Order, OrderItem

    return {
        'db': db,
        'User': User,
        'Product': Product,
        # 'Category': Category,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem
    }


# @app.before_first_request
# def create_tables():
#     """Create database tables if they don't exist"""
#     try:
#         # Import models to ensure they're registered
#         from app.models.user import User
#         from app.models.product import Product
#         from app.models.cart import CartItem
#         from app.models.order import Order, OrderItem
#
#         db.create_all()
#
#         # Check if we have any data, if not, create sample data
#         if not Product.query.first():
#             print("No products found. Please run 'python setup_db.py' first!")
#     except Exception as e:
#         print(f"Error creating tables: {e}")


if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists('instance/ecommerce.db'):
        print("⚠️  Database not found!")
        print("🔧 Please run 'python setup_db.py' first to initialize the database.")
        print("   Then run 'python run.py' to start the application.")
    else:
        print("🚀 Starting Flask E-commerce Application...")
        print("📱 Open your browser to: http://localhost:5000")
        app.run(host="0.0.0.0", port=5000, debug=True)