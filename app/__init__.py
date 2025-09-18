from flask import Flask, redirect, url_for
from app.config import Config
from app.extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login_get'

    # Registrar blueprints (esto no toca modelos directamente)
    from app.views.auth import auth_bp
    from app.views.product import product_bp
    from app.views.cart import cart_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)

    # Importar modelo después de init_app (evita el ciclo)
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.get("/")
    def home():
        return redirect(url_for("product.index"))

    return app