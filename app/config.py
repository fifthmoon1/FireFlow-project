import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # racine du projet

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretjwt")

    # La DB sera dans instance/fireflow.sqlite à la racine
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "instance", "fireflow.sqlite")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
