from flask_jwt_extended import create_access_token


class AuthService:
    @staticmethod
    def create_access_token(email: str):
        return create_access_token(email)
