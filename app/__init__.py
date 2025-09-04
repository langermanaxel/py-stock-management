from flask import Flask, jsonify, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from pathlib import Path
import sqlite3

from .database import db
from .config import Config


def create_app():
    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )
    app.config.from_object(Config)

    # CORS: solo headers (Bearer), sin cookies
    CORS(
        app,
        resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["Authorization"],
    )

    # Inicializar SQLAlchemy y Migrate
    db.init_app(app)
    Migrate(app, db)

    # Configuración JWT (antes de instanciar JWTManager)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    jwt = JWTManager(app)

    # Identidad como string (compat PyJWT 2.x)
    @jwt.user_identity_loader
    def user_identity_lookup(user_or_id):
        return str(user_or_id)

    # Carga de usuario desde JWT usando SQLite directo (si preferís, reemplazar por SQLAlchemy)
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        try:
            user_id = int(jwt_data["sub"])  # identidad viene como string
            db_path = Path(current_app.instance_path) / "stock_management.db"
            if not db_path.exists():
                return None

            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, username, email, password_hash, first_name, last_name,
                           role, is_active, created_at, updated_at, last_login
                    FROM users
                    WHERE id = ? AND is_active = 1
                    """,
                    (user_id,),
                )
                row = cursor.fetchone()

            if not row:
                return None

            class MockUser:
                __slots__ = (
                    "id",
                    "username",
                    "email",
                    "password_hash",
                    "first_name",
                    "last_name",
                    "role",
                    "is_active",
                    "created_at",
                    "updated_at",
                    "last_login",
                )

                def __init__(self, d):
                    (
                        self.id,
                        self.username,
                        self.email,
                        self.password_hash,
                        self.first_name,
                        self.last_name,
                        self.role,
                        is_active,
                        self.created_at,
                        self.updated_at,
                        self.last_login,
                    ) = d
                    self.is_active = bool(is_active)

                def to_dict(self):
                    return {
                        "id": self.id,
                        "username": self.username,
                        "email": self.email,
                        "first_name": self.first_name,
                        "last_name": self.last_name,
                        "role": self.role,
                        "is_active": self.is_active,
                        "created_at": self.created_at,
                        "updated_at": self.updated_at,
                        "last_login": self.last_login,
                    }

            return MockUser(row)

        except Exception as e:
            print(f"Error en user_lookup_callback: {e}")
            return None

    # Handlers JWT en JSON (coherentes con API)
    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify(message="JWT requerido", detail=reason), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify(message="Token inválido", detail=reason), 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify(message="Token expirado"), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(message="Token revocado"), 401

    # Registrar modelos, blueprints y API dentro del app context
    with app.app_context():
        from .models.user import User
        from .models.category import Category
        from .models.product import Product
        from .models.stock import Stock
        from .models.order import Order
        from .models.order_item import OrderItem
        from .models.purchase_order import PurchaseOrder

        from .routes.frontend import frontend_bp
        from .api import init_api

        app.register_blueprint(frontend_bp)  # frontend (templates/static)
        init_api(app)  # API (flask-smorest) — asegúrate del url_prefix que usás

        # No crear tablas aquí. Usar migraciones/scripts separados.

    return app
