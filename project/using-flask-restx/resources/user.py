from flask import abort, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256

from models import UserModel
from blocklist import BLOCKLIST

api = Namespace("users", description="Operations related to users and authentication.")

user_inputs = api.model(
    "UserFields",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

user_outputs = api.model("User", {"id": fields.String(), "username": fields.String()})


@api.route("/register")
class UserRegister(Resource):
    @api.expect(user_inputs, validate=True)
    def post(self):
        user_data = request.get_json()

        if UserModel.find_by_username(user_data["username"]):
            abort(400, "A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        user.save_to_db()

        return {"message": "User created successfully."}, 201


@api.route("/login")
class UserLogin(Resource):
    @api.expect(user_inputs, validate=True)
    def post(self):
        user_data = request.get_json()

        user = UserModel.find_by_username(user_data["username"])

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, "Invalid credentials.")


@api.route("/logout")
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@api.route("/user/<user_id>")
class User(Resource):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @api.marshal_with(user_outputs)
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, "User not found.")
        return user, 200

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, "User not found.")
        user.delete_from_db()
        return {"message": "User deleted."}, 200


@api.route("/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
