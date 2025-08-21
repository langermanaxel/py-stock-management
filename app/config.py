from dotenv import load_dotenv
import os

load_dotenv()

import os

class Config:
    # Obtener la ruta absoluta del directorio actual
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # Construir la ruta completa a la base de datos
    database_path = os.path.join(basedir, 'instance', 'stock_management.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False