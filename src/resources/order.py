from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from utils.validators import role_required
from flask_jwt_extended import get_jwt_identity
from controllers.order_controller import show_all_orders, place_order
from schemas import PlaceOrderSchema


blp = Blueprint("order", __name__, description = "Orders related functionality")


@blp.route("/orders")
class Order(MethodView):

    @jwt_required
    @role_required(["Customer"])
    @blp.arguments(PlaceOrderSchema)
    def post(self, order_info):  
        username = get_jwt_identity()
        return_val = place_order(order_info, username)
        if return_val is None:
            abort(500, message="Internal Server Error!")
        return return_val


    @jwt_required
    @role_required(["Admin"])
    def get(self):
        print("Hello","\n\n\n\n\n\n\n")
        data = show_all_orders()
        if data is None:
            abort(404, message="Orders not available!!!")
        else:
            return {
                "Orders": data
            }, 200