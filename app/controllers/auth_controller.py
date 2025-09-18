from app.models.user import db, User


class UserController:
    @staticmethod
    def get_user_by_email(email: str):
        """Retrieve a user by email, or None if not found"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(username: str, email: str, password: str):
        """Create a new user and save to the database"""
        # Check if email already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            return None  # signal duplicate

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user
