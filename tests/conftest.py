import os
import sys

# Force le répertoire racine (le dossier contenant app/) dans le PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print(">>> PYTHONPATH actif :", sys.path[0])  # Debug

from app import create_app, db
from flask_jwt_extended import create_access_token
import pytest
# Ajoute le dossier racine du projet au PYTHONPATH

print("Current sys.path:", sys.path)
@pytest.fixture()
def app():
    """Créer une app Flask en mode test avec SQLite en mémoire"""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    """Retourne un client Flask pour faire des requêtes"""
    return app.test_client()

@pytest.fixture()
def auth_header(app):
    """Crée un token JWT pour les routes protégées"""
    with app.app_context():
        access_token = create_access_token(identity="test-user")
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "password123"}