import os,bcrypt
from flask import Flask
from flask_restful import Resource, Api
from application.model import Users
from flask_restful import fields, marshal_with,marshal
from flask_restful import reqparse
from application.validation import BusinessValidationError,NotFoundError
from application.database import db
import re


create_register_parser=reqparse.RequestParser()
create_register_parser.add_argument('name')
create_register_parser.add_argument('email')
create_register_parser.add_argument('password')

register_fields={
    "name" : fields.String,
    "email" : fields.String
}

class RegisterAPI(Resource):
    def post(self):
        all_users=Users.query.all()
        # Using List Comprehension to get emails of all users.
        user_list=[user.email for user in all_users]
        for i in all_users:
            user_list.append(i.email)
        args=create_register_parser.parse_args()
        print(args)

        Email=args.get('email')
        # Using RegEx module to validate email
        valid_email=re.findall("@gmail.com$", Email) 
        if not valid_email:
            return {'message' : 'Please enter valid email'},400
            
        if Email in user_list:
            return {"message" : "Email already exists"} ,200
            
        Name=args.get('name')
        password=args.get('password')
        print(password)
        if password:
            if (len(password) >= 8 and re.search(r'[0-9]', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
                # Encode the password to bytes before encrypting
                password = password.encode('utf-8')
            else:
                return {'message':"Password must be at least 8 characters long, contain at least one special character, and one number"}, 400
        else:
            raise BusinessValidationError(status_code=404 ,error_code='' ,error_message='Password is required')
        
        if Email is None:
            raise BusinessValidationError(status_code=404 ,error_code='' ,error_message='Email is required')
        if Name is None :
            raise BusinessValidationError(status_code=404,error_code='' ,error_message='Name is required')
        
        else:
            user=Users(email=Email,name=Name,password= bcrypt.hashpw(password, bcrypt.gensalt()) )
            db.session.add(user)
            print(2)
            db.session.commit()
            print(3)

        return marshal(user ,register_fields)






