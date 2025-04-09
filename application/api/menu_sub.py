from flask_restful import Resource ,reqparse,marshal,fields,request
from application.validation import *
from application.database import *
from application.model import *

create_sub_parser=reqparse.RequestParser()
create_sub_parser.add_argument('title')
create_sub_parser.add_argument('menu_id')

update_sub_parser=reqparse.RequestParser()
update_sub_parser.add_argument('title')

menu_sub_fields={
    'id' :fields.Integer,
    'title':fields.String,
    'menu_id':fields.Integer
}

class Menu_SubAPI(Resource):
    def get(self,id=None):
        if id :
            menu_sub=db.session.query(Menu_Sub).filter(Menu_Sub.id==id).first()
            if not menu_sub:
                return {'message' :'No category found with given id.'},404
            return marshal(menu_sub,menu_sub_fields),200
        
        # Check if menu_id is passed as a query parameter
        args=create_sub_parser.parse_args()
        menu_id=args.menu_id
        # menu_id =args.get('menu_id')
        if menu_id:
            menu_subs = db.session.query(Menu_Sub).filter(Menu_Sub.menu_id == menu_id).all()
            return marshal(menu_subs, menu_sub_fields),200
        else:
            all_menu_sub=Menu_Sub.query.all()
            return marshal(all_menu_sub,menu_sub_fields),200

    def put(self,id):
        menu_sub=db.session.query(Menu_Sub).filter(Menu_Sub.id==id).first()
        if not menu_sub:
            return {'message' :'No category found with given id.'}
        args=update_sub_parser.parse_args()
        title=args.get('title')
        if not title:
            return {'message' :'no title given to update'}
        menu_sub.title=title
        db.session.commit()
        
        return marshal(menu_sub,menu_sub_fields)

    def delete(self,id):
        menu_sub=db.session.query(Menu_Sub).filter(Menu_Sub.id==id).first()
        if not menu_sub:
            return {'message' :'No category found with given id.'}
        db.session.delete(menu_sub)
        db.session.commit()
        
        return {'message':"deleted successfully"}

    def post(self):
        args=create_sub_parser.parse_args()
        title=args.get('title')
        if not title:
            raise BusinessValidationError(status_code=404 ,error_code='',error_message='Please provide title')
        
        menu_id=args.get('menu_id')
        menu=db.session.query(Menu).filter(Menu.id==menu_id).first()
        if not menu:
            raise NotFoundError
        
        menu_sub=Menu_Sub(title=title,menu_id=menu_id)
        db.session.add(menu_sub)
        db.session.commit()
        
        return marshal(menu_sub,menu_sub_fields)