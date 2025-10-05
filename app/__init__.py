from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt

from flask_restx import Api

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Entrez votre JWT avec 'Bearer <token>'"
    }
}

from flask import Flask
from .extensions import db, migrate, jwt
from .config import Config
from flask_restx import Api
from fireflow.routes import ns as firewall_ns
from users.routes import ns as users_ns
from dotenv import load_dotenv


load_dotenv()  # charge le fichier .env automatiquement

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Si une configuration personnalisée est passée (ex: pour les tests)
    if config:
        app.config.update(config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # API + Swagger
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }

    api = Api(
        app,
        version="1.0",
        title="Fireflow API",
        description="API avec JWT + Firewalls",
        authorizations=authorizations,
        security='Bearer Auth'
    )

    api.add_namespace(firewall_ns, path="/fireflow")
    api.add_namespace(users_ns, path="/users")

    return app

