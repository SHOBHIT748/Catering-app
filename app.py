
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
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Fetch variables
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG")
db_url = os.getenv("DATABASE_URL")

app = None
api = None
jwt = None  # JWT manager instance

cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET")
)


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(os.getenv("JWT_EXP_MINUTES", 30)))

    db.init_app(app)
    api = Api(app)
    global jwt
    # Initialize JWT manager
    jwt = JWTManager(app)  
    # Iniatilize Flask-migrate
    migrate=Migrate(app,db)

    app.app_context().push()

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

from application.api.testimonial import TestimonialAPI
api.add_resource(TestimonialAPI,'/api/testimonial','/api/testimonial/<int:id>')

from application.api.booking import BookingAPI
api.add_resource(BookingAPI ,'/api/booking' ,'/api/booking/<int:id>')

from application.api.checkout import CheckOutAPI
api.add_resource(CheckOutAPI ,'/api/checkout','/api/checkout/<int:id>')


if __name__ == "__main__":
    app.run(debug=True)

