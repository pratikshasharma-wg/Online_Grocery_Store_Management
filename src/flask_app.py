import logging
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from resources.login import blp as login
from resources.order import blp as order
from resources.logout import blp as logout
from resources.wallet import blp as wallet
from resources.product import blp as product
from resources.register import register_blp as register


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.DEBUG,
    filename="src\\config\\logs.txt",
)

logger = logging.getLogger("main")


if __name__ == "__main__":

    app = Flask(__name__)
    app.config["API_TITLE"] = "Grocery Store"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["JWT_SECRET_KEY"] = "pratiksha"

    api = Api(app)

    jwt = JWTManager(app)

    api.register_blueprint(login)
    api.register_blueprint(register)
    api.register_blueprint(product)
    api.register_blueprint(logout)
    api.register_blueprint(order)
    api.register_blueprint(wallet)

    app.run(debug=True, port=5000)
