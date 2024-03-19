import pymongo
from flask import Flask
from flask_jwt_extended import JWTManager
import mimetypes
import uuid
import os

from src import getConfig
from src.auth.Users import Users ,customError
from blueprints import userapi ,productapi,orderapi
app = Flask(__name__)
jwt = JWTManager(app)
app.secret_key=getConfig('secret_Key')
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "HEJVEVNWEiofowejfoiwfwfFJWEIF")
app.register_blueprint(userapi.bp)
app.register_blueprint(productapi.bp)
app.register_blueprint(orderapi.bp)

@app.route('/hello')
def hello_world():
   return 'Hello World'

if __name__ == '__main__':
   app.run(debug=True)