from flask import Flask, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from utils.validators import role_required
from controllers.product_controller import add_product, delete_product, update_product
from controllers.product_controller import show_all_products
from schemas import AddProductSchema, UpdateProductSchema


blp = Blueprint("product", __name__, description = "operations on product")

@blp.route("/product")
@blp.route("/product/<int:product_id>")
class Product(MethodView):

    @jwt_required()
    @role_required(["Admin"])
    @blp.arguments(AddProductSchema)
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def post(self, product_info, product_id=None):
        if product_id is None:
            return_val = add_product(
                product_info["product_name"],
                product_info["product_price"],
                product_info["product_quantity"]
            )

            if return_val is True:
                return jsonify({
                    "message": "New product added successfully!",
                })
        abort(400, message = "Product not added!")


    @jwt_required()
    @role_required(["Admin"])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def delete(self, product_id):
        if product_id:
            return_val = delete_product(product_id)
            if return_val is True:
                return {
                    "message": f"Product with Product id:{product_id} deleted successfully!!!"
                }, 200
        abort(400, message = "Product does not exists!!!")


    @role_required(["Admin"])
    @blp.arguments(UpdateProductSchema)
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def put(self, product_info, product_id):

        product_name = None
        product_price = None
        product_quantity = None

        if product_id:

            if "product_name" in product_info:
                product_name = product_info['product_name']
            if "product_price" in product_info:
                product_price = product_info['product_price']
            if "product_quantity" in product_info:
                product_quantity = product_info['product_quantity']

            return_val = update_product(
                product_id,
                product_name,
                product_price,
                product_quantity
            )
            if return_val is True:
                return {
                    "message": "Product details updated successfully!"
                }, 200
        abort(400, message = "Try again!")


    @role_required(["Admin", "Customer"])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self, product_id = None):
        if not product_id:
            return_val = show_all_products()
            if return_val is not None:
                return {
                    "Products": return_val
                }       
        abort(400, message = "Try again!")