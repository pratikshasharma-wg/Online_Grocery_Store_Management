import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import LoginUserSchema
from controllers.auth import login
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

blp = Blueprint("login", __name__, description = "Login user")

@blp.route("/login")
class Login(MethodView):

    @blp.arguments(LoginUserSchema)
    def post(self, user_info):
        user_data = login(user_info["email"], user_info["password"])
        if user_data is None:
            abort(400, message = "Can't log in...")
        elif user_data[0] == False:
            return {
                "code": 401,
                "status": "Unauthorized",
            }, 401
        else:
            access_token = create_access_token(
            identity = user_data[2],
            additional_claims = {"role": user_data[1]}
            )
            
            return {
                "message":"logged in successfully",
                "access_token": access_token
            }, 200