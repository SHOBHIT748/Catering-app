
import bcrypt, os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from application.database import db
from application.config import LocalDevelopmentConfig
from application.model import *
from datetime import timedelta
import cloudinary
from flask_migrate import Migrate

app = None
api = None
jwt = None  # JWT manager instance

# Cloudinary configuration
cloudinary.config(
    cloud_name='dzz6eozxw' ,
    api_key='954466492996241' ,
    api_secret='Iq6D6DmN2uC1pnkK_i9565GVpg0'
)

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)

    app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this to a strong secret key in production

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)  # Token expires after 30 minutes


    db.init_app(app)
    api = Api(app)
    global jwt
    # Initialize JWT manager
    jwt = JWTManager(app)  
    # Iniatilize Flask-migrate
    migrate=Migrate(app,db)

    app.app_context().push()

    # Automatically create all tables (Not recommended for production)
    # with app.app_context():
    #     print('Creating database')
    #     db.create_all()
    #     print('Database created successfully')
    return app, api

app, api = create_app()


from application.controllers import *

from application.api.user import RegisterAPI
api.add_resource(RegisterAPI, '/api/register')

from application.api.services import ServicesAPI
api.add_resource(ServicesAPI,'/api/services','/api/services/<int:id>')

from application.api.menu import MenuAPI
api.add_resource(MenuAPI,'/api/menu','/api/menu/<int:id>')

from application.api.menu_sub import Menu_SubAPI
api.add_resource(Menu_SubAPI,'/api/menu_sub','/api/menu_sub/<int:id>')

from application.api.menu_item import MenuItemAPI
api.add_resource(MenuItemAPI,'/api/menu_item','/api/menu_item/<int:id>')

from application.api.contact import ContactAPI
api.add_resource(ContactAPI,'/api/contact')

from application.api.gallery import galleryAPI
api.add_resource(galleryAPI,'/api/gallery')


# ✅ Login Route (JWT Authentication)
@app.route("/api/login", methods=["POST"])
def login(): 

    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = Users.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401


# ✅ Protected Route Example
@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200


if __name__ == "__main__":
    app.run(debug=True)

