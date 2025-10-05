
from app import db
from users.models import User


import pytest
from app import create_app, db
from users.models import User
from flask_jwt_extended import decode_token


def test_register_user(client):
    data = {"username": "testuser", "password": "password123"}
    response = client.post("/users/register", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "User created"
    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert user.check_password("password123")

def test_register_existing_user(client):
    user = User(username="existing")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    data = {"username": "existing", "password": "newpass"}
    response = client.post("/users/register", json=data)
    assert response.status_code == 400
    assert response.json["message"] == "User already exists"

def test_register_invalid_json(client):
    response = client.post("/users/register", data="not a json", headers={"Content-Type": "text/plain"})
    # Flask/RESTX retourne 415 si Content-Type != application/json
    assert response.status_code in [400, 415]

def test_login_user(client):
    user = User(username="loginuser")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    data = {"username": "loginuser", "password": "password"}
    response = client.post("/users/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json
    # Vérifie que le token est décodable
    token_data = decode_token(response.json["access_token"])
    assert token_data["sub"] == str(user.id)

def test_login_invalid_credentials(client):
    data = {"username": "nonexistent", "password": "wrong"}
    response = client.post("/users/login", json=data)
    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials"

def test_login_invalid_json(client):
    response = client.post("/users/login", data="invalid", headers={"Content-Type": "text/plain"})
    assert response.status_code in [400, 415]
