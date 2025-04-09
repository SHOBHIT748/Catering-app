from flask import request,redirect,render_template,url_for,current_app as app
from flask_login import login_user,logout_user,current_user,LoginManager
from application.database import db
from application.model import Users
import bcrypt
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with,marshal
from flask_restful import reqparse




# # LoginManager is needed for our application 
# # to be able to log in and out users
# login_manager = LoginManager()
# login_manager.init_app(app)


# # Creates a user loader callback that returns the user object given an id
# @login_manager.user_loader
# def loader_user(user_id):
#     return db.session.Users.query.get(user_id)

# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         # Hash the password using bcrypt
#         password = request.form.get("password").encode('utf-8')  # Encode password to bytes
#         hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())  # Hash the password

#         # Create the user and store in the database
#         user =Users(username=request.form.get("username"), password=hashed_password.decode('utf-8'))  # Decode the hash to a string
#         db.session.add(user)
#         db.session.commit()

#         # Redirect to login after successful registration
#         return marshal(user)
    
#     return render_template("sign_up.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         user =Users.query.filter_by(username=request.form.get("username")).first()

#         if user:
#             # Check if the entered password matches the hashed password
#             entered_password = request.form.get("password").encode('utf-8')
#             if bcrypt.checkpw(entered_password, user.password.encode('utf-8')):
#                 login_user(user)
#                 # return redirect(url_for("home"))
#                 return redirect(url_for("user_dash"))
                
        
#         # In case of incorrect login
#         return "Invalid login credentials"

#     return render_template("login.html")

# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")

# @app.route('/user_dash')
# def user_dash():
#     return render_template('home.html',username=current_user.username)