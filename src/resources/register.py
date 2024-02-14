from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import RegisterUserSchema
from controllers import auth

register_blp = Blueprint("register", __name__, description="Register user")


@register_blp.route("/register")
class Register(MethodView):

    @register_blp.arguments(RegisterUserSchema)
    def post(self, user_info):
        return_val = auth.signUp(
            user_info["name"],
            user_info["email"],
            user_info["password"],
            user_info["wallet_status"],
        )

        if return_val is None:
            abort(400, message="Cannot be registered!!!")
        else:
            return {
                "message": f"User with email:{user_info['email']} Registered Successfully!!!"
            }, 201
