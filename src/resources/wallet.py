from flask.views import MethodView
from utils.validators import role_required
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import WalletSchema
from controllers import order_controller


blp = Blueprint("wallet", __name__, description="Money in wallet")


@blp.route("/wallet")
class Wallet(MethodView):

    @jwt_required()
    @role_required(["Customer"])
    @blp.doc(
        parameters=[
            {
                "name": "Authorization",
                "in": "header",
                "description": "Authorization: Bearer <access_token>",
                "required": "true",
            }
        ]
    )
    def get(self):
        username = get_jwt_identity()
        wallet_amount = order_controller.user.get_wallet(username)
        if wallet_amount:
            return {"email": username, "wallet_amount": wallet_amount}, 200
        else:
            abort(400, message="Try again!")

    @jwt_required
    @role_required(["Customer"])
    @blp.arguments(WalletSchema)
    @blp.doc(
        parameters=[
            {
                "name": "Authorization",
                "in": "header",
                "description": "Authorization: Bearer <access_token>",
                "required": "true",
            }
        ]
    )
    def put(self, amount):
        username = get_jwt_identity()
        return_val = order_controller.update_wallet(username, amount)
        if return_val:
            return {
                "email": username,
                "message": f"Amount of Rs.{amount} added to the wallet successfully!",
            }, 200
