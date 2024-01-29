import sys
import logging
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from resources.login import blp as login
from resources.register import register_blp as register
from resources.product import blp as admin
from resources.logout import blp as logout


logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level = logging.DEBUG,
                    filename = 'src\\config\\logs.txt')

logger = logging.getLogger('main')
   
    
if __name__ == "__main__":  

    app = Flask(__name__)
    app.config["API_TITLE"] = "Grocery Store"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    api = Api(app)
 
    app.config["JWT_SECRET_KEY"] = "pratiksha"
    jwt = JWTManager(app)
    api.register_blueprint(login)
    api.register_blueprint(register)
    api.register_blueprint(admin)
    api.register_blueprint(logout)
   
    app.run(debug=True, port = 5000)
   