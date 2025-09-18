from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from app.extensions import login_manager 
from app.controllers.auth_controller import UserController
from typing import Optional

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class MockUser(UserMixin):
    def __init__(self, id: int, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self._password = password 
        
    def check_password(self, pw: str) -> bool:
        return self._password == pw

_MOCK_USERS_BY_ID = {}
_MOCK_USERS_BY_EMAIL = {}
_next_id = 1

def _create_user(name: str, email: str, password: str) -> MockUser:
    global _next_id
    u = MockUser(id=_next_id, name=name, email=email, password=password)
    _MOCK_USERS_BY_ID[str(u.id)] = u
    _MOCK_USERS_BY_EMAIL[email] = u
    _next_id += 1
    return u

def _get_by_email(email: str) -> Optional[MockUser]:
    return _MOCK_USERS_BY_EMAIL.get(email)

# if not _MOCK_USERS_BY_EMAIL:
#     _create_user("Usuario Demo", "demo@demo.com", "demo123")

@login_manager.user_loader
def load_user(user_id: str):
    return _MOCK_USERS_BY_ID.get(str(user_id))

@auth_bp.get("/login")
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for("product.index"))
    return render_template("auth/login.html")

@auth_bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # user = _get_by_email(email)
    user = UserController.get_user_by_email(email)
    if not user or not user.check_password(password):
        flash("Credenciales inválidas", "error")
        return redirect(url_for("auth.login_get"))

    login_user(user, remember=bool(request.form.get("remember")))
    flash("Sesión iniciada", "success")
    next_url = request.args.get("next") or url_for("product.index")
    return redirect(next_url)

@auth_bp.get("/register")
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for("product.index"))
    return render_template("auth/register.html")

@auth_bp.post("/register")
def register_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    if not name or not email or not password:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for("auth.register_get"))
    if password != confirm:
        flash("Las contraseñas no coinciden", "error")
        return redirect(url_for("auth.register_get"))
    if UserController.get_user_by_email(email):
        flash("El correo ya está registrado", "error")
        return redirect(url_for("auth.register_get"))

    UserController.create_user(username=name, email=email, password=password)
    flash("Cuenta creada. Inicia sesión.", "success")
    return redirect(url_for("auth.login_get"))


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "success")
    return redirect(url_for("auth.login_get"))