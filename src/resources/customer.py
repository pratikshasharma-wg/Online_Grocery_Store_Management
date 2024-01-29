from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from utils.validators import role_required
from controllers.product_controller import add_product, show_all_avail_prod
from schemas import ProductSchema, OrderSchema


blp = Blueprint("order", __name__, description = "Orders related functionality")

@blp.route("/products")
class Order(MethodView):

    # @jwt_required
    # @role_required(["Customer"])
    # @blp.arguments(OrderSchema)
    # def post(self, order_info):

    def get(self):
        data = show_all_avail_prod()
        if data is None:
            return {
                "message": "No products available!"
            }
        return {
            "Products": [data]
        }
        

    # @jwt_required
    # @role_required(["Customer"])
    # def get(self):
    #     pass