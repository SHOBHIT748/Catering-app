from flask_restful import Resource,reqparse,marshal,fields
from application.validation import *
from application.model import *

create_contact_parser=reqparse.RequestParser()
create_contact_parser.add_argument('name')
create_contact_parser.add_argument('email')
create_contact_parser.add_argument('phone_number')
create_contact_parser.add_argument('query')

contact_fields={
    'name':fields.String,
    'email':fields.String,
    'phone_number':fields.String,
    'query':fields.String
}


class ContactAPI(Resource):
    def post(self):
        args=create_contact_parser.parse_args()
        name=args.get('name')
        email=args.get('email')
        phone_number=args.get('phone_number')
        query=args.get('query')
        if not name :
            raise BusinessValidationError(status_code=404,error_code='',error_message='name is required')
        if not email :
            raise BusinessValidationError(status_code=404,error_code='',error_message='email is required')
        if not phone_number :
            raise BusinessValidationError(status_code=404,error_code='',error_message='phone_no is required')
        if not query :
            raise BusinessValidationError(status_code=404,error_code='',error_message='query is required')
        
        new_contact=Contact(name=name,email=email,phone_number=phone_number,query=query)
        db.session.add(new_contact)
        db.session.commit()

        return marshal(new_contact,contact_fields)

