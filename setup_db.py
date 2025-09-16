# File: setup_db.py
"""
Database setup script for Flask E-commerce application
Run this BEFORE starting the main application for the first time
"""

from app import create_app, db


def initialize_database():
    """Initialize database with tables and sample data"""
    app = create_app()

    with app.app_context():
        # Import all models to ensure they're registered
        from app.models.user import User
        from app.models.product import Product
        from app.models.cart import CartItem
        from app.models.order import Order, OrderItem

        print("Dropping existing tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        print("Creating sample data...")

        db.session.flush()  # Get IDs without committing

        # Create sample products
        products = [
            # Electronics
            Product(name='Smartphone',
                    description='Latest smartphone with advanced camera and long battery life',
                    price=599.99, stock=15),
            Product(name='Laptop',
                    description='High-performance laptop perfect for work and gaming',
                    price=1299.99, stock=8),
            Product(name='Wireless Headphones',
                    description='Premium noise-cancelling wireless headphones',
                    price=199.99, stock=25),
            Product(name='Tablet',
                    description='10-inch tablet with stunning display',
                    price=299.99, stock=12),

            # Toys
            Product(name='Robot Toy',
                    description='Interactive robot toy that responds to voice commands',
                    price=49.99, stock=30),
            Product(name='Building Blocks Set',
                    description='Creative building blocks for hours of fun',
                    price=24.99, stock=40),
            Product(name='Remote Control Car',
                    description='Fast RC car with LED lights and sound effects',
                    price=79.99, stock=18),
            Product(name='Puzzle Game',
                    description='1000-piece jigsaw puzzle with beautiful artwork',
                    price=19.99, stock=22),

            # Books
            Product(name='Python Programming Guide',
                    description='Complete guide to Python programming for beginners',
                    price=39.99, stock=20),
            Product(name='Web Development Handbook',
                    description='Modern web development with HTML, CSS, and JavaScript',
                    price=44.99, stock=15),
            Product(name='Data Science Essentials',
                    description='Learn data science with practical examples',
                    price=54.99, stock=10),

            # Clothing
            Product(name='Cotton T-Shirt',
                    description='Comfortable cotton t-shirt in various colors',
                    price=19.99, stock=50),
            Product(name='Denim Jeans',
                    description='Classic denim jeans with perfect fit',
                    price=59.99, stock=25),
            Product(name='Winter Jacket',
                    description='Warm winter jacket with water resistance',
                    price=129.99, stock=12),
        ]

        db.session.add_all(products)

        # Create a sample admin user
        admin_user = User(username='admin', email='admin@toystore.com')
        admin_user.set_password('admin123')

        # Create a sample regular user
        demo_user = User(username='demo', email='demo@toystore.com')
        demo_user.set_password('demo123')

        db.session.add_all([admin_user, demo_user])

        # Commit all changes
        db.session.commit()

        print(f"✅ Database initialized successfully!")
        print(f"🛍️ Created {Product.query.count()} products")
        print(f"👥 Created {User.query.count()} users")
        print()
        print("Sample users created:")
        print("  Username: admin, Password: admin123")
        print("  Username: demo, Password: demo123")
        print()
        print("🚀 You can now run: python run.py")


if __name__ == '__main__':
    initialize_database()