from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from controllers.auth import login
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

blp = Blueprint("logout", __name__, description="Logout user")

BLOCKLIST = set()


@blp.route("/logout")
class Logout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
