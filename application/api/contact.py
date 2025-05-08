from flask_restful import Resource,reqparse,marshal,fields
from application.validation import *
from application.model import Contact
from application.database import db
from sqlalchemy import desc
import re

create_contact_parser=reqparse.RequestParser()
create_contact_parser.add_argument('name')
create_contact_parser.add_argument('email')
create_contact_parser.add_argument('phone_number')
create_contact_parser.add_argument('query')

contact_fields={
    "id":fields.Integer,
    'name':fields.String,
    'email':fields.String,
    'phone_number':fields.String,
    'query':fields.String
}


class ContactAPI(Resource):
    def get(self):
        # all_gallery=Gallery.query.order_by(desc(Gallery.id)).all()
        all_contact=db.session.query(Contact).order_by(desc(Contact.id)).all()
        return [marshal(contact, contact_fields) for contact in all_contact]

    def delete(self,id):
        contact=db.session.query(Contact).filter(Contact.id==id).first()
        if not contact:
            raise BusinessValidationError(status_code=404 ,error_code='' ,error_message='No such contact')
        db.session.delete(contact)
        db.session.commit()

        return {'message':'deleted successfully'}

    def post(self):
        args=create_contact_parser.parse_args()
        name=args.get('name')
        email=args.get('email')
        # Using RegEx module to validate email
        valid_email=re.findall("@gmail.com$", email)
        if not valid_email:
            return {'message' : 'Please enter valid email'},400

        phone_number=args.get('phone_number')
        #  print(password)
        if phone_number:
            if (len(phone_number) == 10 and re.fullmatch(r'\d{10}',phone_number)):
                pass
            else:
                return {'message':"Phone number must have exactly 10 digits"}, 400
        query=args.get('query')
        if not name :
            raise BusinessValidationError(status_code=404,error_code='',error_message='name is required')
        if not email :
            raise BusinessValidationError(status_code=404,error_code='',error_message='email is required')
        if not phone_number :
            raise BusinessValidationError(status_code=404,error_code='',error_message='phone_number is required')
        if not query :
            raise BusinessValidationError(status_code=404,error_code='',error_message='query is required')

        new_contact=Contact(name=name,email=email,phone_number=phone_number,query=query)
        db.session.add(new_contact)
        db.session.commit()

        return marshal(new_contact,contact_fields)

