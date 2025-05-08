import os
from app import app
from flask import render_template, request, jsonify, url_for
from application.model import Users
import bcrypt
from application.database import db
from application.validation import BusinessValidationError
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
import re
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

# ✅ LOGIN ROUTE
@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = Users.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=email)
        return jsonify(id=user.id ,access_token=access_token ,role=user.role), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401


# ✅ RESET TOKEN GENERATOR
def generate_reset_token(email, secret_key, salt='password-reset-salt'):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def confirm_reset_token(token, secret_key, salt='password-reset-salt', expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
    except Exception:
        return None
    return email


def send_reset_email(email, token):
    frontend_base_url = os.getenv('FRONTEND_BASE_URL')
    reset_url = f"{frontend_base_url}/reset/{token}"

    subject = "Reset Your Password"
    body = f"Hi,\n\nClick the link below to reset your password:\n{reset_url}\n\nThis link will expire in 1 hour."

    message = MIMEMultipart()
    message["From"] = os.getenv('EMAIL_USER')
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", int(os.getenv('EMAIL_PORT')) )as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USER') ,os.getenv('EMAIL_PASS'))
            server.sendmail(os.getenv('EMAIL_USER'), email, message.as_string())
            print("Reset email sent!")
    except Exception as e:
        print("Failed to send email:", e)


# ✅ FORGOT PASSWORD (Send Email)
@app.route('/api/forgot', methods=['POST'])
def forgot():
    email = request.json.get('Email')
    user = Users.query.filter_by(email=email).first()
    if not user:
        raise BusinessValidationError(status_code=404, error_code=' ', error_message='Email not registered')

    token = generate_reset_token(email, app.config['SECRET_KEY'])
    send_reset_email(email, token)

    return jsonify({"message": "Password reset link sent to your email."}), 200


# ✅ RESET PASSWORD (PUT from Axios or Postman)
@app.route('/api/reset/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('password')
    confirm_password = data.get('confirm_password')

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    email = confirm_reset_token(token, app.config['SECRET_KEY'])
    if not email:
        return jsonify({"message": "Invalid or expired token"}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully!"}), 200

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    email = get_jwt_identity()
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "name": user.name,
        "email": user.email
    }), 200


# Profile update
@app.route('/api/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    email = get_jwt_identity()  # Get user email from JWT
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    # You can update these fields as needed
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully!"}), 200

# Change password
@app.route('/api/change_password' ,methods=['PUT'])
@jwt_required()
def change_password():
    email=get_jwt_identity()  # Get user email from JWT
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    data=request.get_json()

    old_password=data.get('old password')
    new_password=data.get('new password')
    confirm_password=data.get('confirm password')

    if not (user and bcrypt.checkpw(old_password.encode('utf-8'), user.password)):
        return {'message' : 'old password does not match'}

    if  new_password:
            if (len(new_password) >= 8 and re.search(r'[0-9]', new_password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password)):
                # Encode the password to bytes before encrypting
                new_password = new_password.encode('utf-8')
            else:
                return {'message':"New Password must be at least 8 characters long, contain at least one special character, and one number"}, 400

    if  confirm_password:
            # if (len(new_password) >= 8 and re.search(r'[0-9]', confirm_password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password)):
                # Encode the password to bytes before encrypting
                confirm_password = confirm_password.encode('utf-8')
    if new_password!=confirm_password :
        return {'message':'password does not match'}

    user.password=bcrypt.hashpw(new_password, bcrypt.gensalt())
    db.session.commit()

    return jsonify({'message' :'Password updated successfully'})




# ✅ HOME (Optional)
@app.route('/')
def home():
    return render_template('build/index.html')


# ✅ CATCH-ALL FOR FRONTEND ROUTING (React/Vue etc.)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('build/index.html')