from flask_restful import Resource ,fields ,marshal ,reqparse
from application.model import Booking
from application.database import db
from datetime import datetime
from application.validation import BusinessValidationError


create_booking_parser=reqparse.RequestParser()
create_booking_parser.add_argument('name',required=True ,help='name is missing')
create_booking_parser.add_argument('phone_no',required=True ,help='phone_no is missing')
create_booking_parser.add_argument('occasion',required=True ,help='occasion is missing')
create_booking_parser.add_argument('dishes',required=True ,help='dishes is missing')
create_booking_parser.add_argument('date',required=True ,help='date is missing')
create_booking_parser.add_argument('message')

booking_fields={
    'name' :fields.String ,
    'phone_no' : fields.String ,
    'occasion' : fields.String ,
    'dishes' :fields.String ,
    'timestamp' :fields.DateTime ,
    'message' :fields.String
    }

class BookingAPI(Resource):
    def get(self,id):
        booking=Booking.query.filter_by(id=id).first()
        if not booking :
            raise BusinessValidationError(status_code=404 ,error_code=' ' ,error_message='No booking found with given id')
        return marshal(booking ,booking_fields)


    def post(self):
        args=create_booking_parser.parse_args()

        name=args.get('name')
        phone_no=args.get('phone_no')
        occasion=args.get('occasion')
        dishes=args.get('dishes')
        date=args.get('date')
        date_obj = datetime.strptime(date, "%d-%m-%Y %H:%M")
        message=args.get('message')

        booking=Booking(name=name ,phone_no=phone_no ,occasion=occasion ,dishes=dishes ,timestamp=date_obj ,message=message)

        db.session.add(booking)
        db.session.commit()

        return marshal(booking ,booking_fields)