from flask_restful import Resource,reqparse,marshal,fields
from application.validation import *
from application.model import Testimonial
from application.database import db
from sqlalchemy import desc

create_testimonial_parser=reqparse.RequestParser()
create_testimonial_parser.add_argument('name')
create_testimonial_parser.add_argument('description')

update_testimonial_parser=reqparse.RequestParser()
update_testimonial_parser.add_argument('new name')
update_testimonial_parser.add_argument('new description')

testimonial_fields={
    'id': fields.Integer,
    'name':fields.String,
    'description': fields.String
}

class TestimonialAPI(Resource):
    def get(self):
        all_testimonial=Testimonial.query.order_by(desc(Testimonial.id)).all()

        return [marshal(testimonial,testimonial_fields) for testimonial in all_testimonial]

    def put(self,id):
        testimonial=db.session.query(Testimonial).filter(Testimonial.id==id).first()
        if not testimonial:
            return {'message':'no such testimonial'}
        args=update_testimonial_parser.parse_args()
        new_name=args.get('new name')
        new_description=args.get('new description')
        if not new_name:
            raise BusinessValidationError(status_code=404,error_code=' ' ,error_message='name is required')
        if not new_description:
            raise BusinessValidationError(status_code=404,error_code=' ' ,error_message='description is required')
        testimonial.name=new_name
        testimonial.description=new_description

        db.session.commit()
        return marshal(testimonial,testimonial_fields)


    def delete(self,id):
        testimonial=db.session.query(Testimonial).filter(Testimonial.id==id).first()
        if not testimonial:
            return {'message':'no such testimonial'}
        db.session.delete(testimonial)
        db.session.commit()

        return {'message':'testimonial deleted successfully'}
    def post(self):
        args=create_testimonial_parser.parse_args()
        name=args.get('name')
        description=args.get('description')
        if not name:
            raise BusinessValidationError(status_code=404,error_code=' ' ,error_message='name is required')
        if not description:
            raise BusinessValidationError(status_code=404,error_code=' ' ,error_message='description is required')

        new_testimonial=Testimonial(name=name ,description=description)
        db.session.add(new_testimonial)
        db.session.commit()

        return marshal(new_testimonial,testimonial_fields)
