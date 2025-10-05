from flask_restx import Namespace, Resource, fields
from flask import request
from app.extensions import db
from flask_jwt_extended import create_access_token
from .models import User
from .schemas import UserSchema

ns = Namespace("users", description="Gestion des utilisateurs et authentification")

user_schema = UserSchema()
login_model = ns.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})
register_model = ns.model("Register", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

@ns.route("/register")
class Register(Resource):
    @ns.expect(register_model, validate=True)
    def post(self):
        data = request.json
        errors = user_schema.validate(data)
        if errors:
            return {"errors": errors}, 400
        if User.query.filter_by(username=data["username"]).first():
            return {"message": "User already exists"}, 400
        user = User(username=data["username"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created"}, 201

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.check_password(data["password"]):
            return {"message": "Invalid credentials"}, 401
        token = create_access_token(identity=str(user.id))
        return {"access_token": token}, 200
