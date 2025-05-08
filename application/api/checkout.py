from flask_restful import Resource, marshal, fields, reqparse
from application.validation import BusinessValidationError
from application.model import Checkout
from application.database import db
# from flask import jsonify

# Request parser setup
create_checkout_parser = reqparse.RequestParser()
create_checkout_parser.add_argument('cartitems', type=dict, action='append', required=True, help='cartitems are required')
create_checkout_parser.add_argument('userinfo', type=dict, required=True, help='userinfo is required')
create_checkout_parser.add_argument('total_dishes', type=int, required=True, help='total_dishes is required')
create_checkout_parser.add_argument('total_persons', type=int, required=True, help='total_persons is required')

# Output structure
checkout_fields = {
    'id'      : fields.Integer,
    'cartitems': fields.Raw,
    'userinfo': fields.Raw,
    'total_dishes': fields.Integer,
    'total_persons': fields.Integer
}

class CheckOutAPI(Resource):
    def get(self):
        all_checkouts=Checkout.query.all()
        return marshal(all_checkouts ,checkout_fields)

    def delete(self,id):
        checkout=Checkout.query.filter_by(id=id).first()
        if not checkout:
            return {'message' :'no checkout with given id '}
        db.session.delete(checkout)
        db.session.commit()
        return {'message':'deleted successfully'}

    def post(self):
        args = create_checkout_parser.parse_args()

        cart_items = args.get('cartitems')
        form_data = args.get('userinfo')
        total_dishes = args.get('total_dishes')
        total_persons = args.get('total_persons')

        # Validate form fields
        required_fields = ['name', 'phone', 'address','occasion', 'pincode', 'city',"state", 'payment_method']
        for field in required_fields:
            if not form_data.get(field):
                raise BusinessValidationError(
                    status_code=400,
                    error_code='MISSING_FIELD',
                    error_message=f'Please provide {field}'
                )

        # Save to DB
        checkout = Checkout(
            cartitems=cart_items,
            userinfo=form_data,
            total_dishes=total_dishes,
            total_persons=total_persons
        )
        db.session.add(checkout)
        db.session.commit()

        return marshal(checkout ,checkout_fields)
