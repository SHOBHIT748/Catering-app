from flask_restful import Resource,fields,reqparse ,marshal
from application.validation import *
from application.database import *
from application.model import *


create_menu_parser=reqparse.RequestParser()
create_menu_parser.add_argument('title')

update_menu_parser=reqparse.RequestParser()
update_menu_parser.add_argument('title')

menu_fields={
    "id": fields.Integer,
    "title" : fields.String
}

class MenuAPI(Resource):
    def get(self,id=None):
        if id :
            menu=db.session.query(Menu).filter(Menu.id==id).first()
            if not menu:
                return {'message' :"No menu with given id."}
            return marshal(menu,menu_fields)
        else:
            all_menu=Menu.query.all()
            for i in all_menu:
                print(i.title)
            return [marshal(menu,menu_fields) for menu in all_menu]

    def put(self,id):
        menu=db.session.query(Menu).filter(Menu.id==id).first()
        if not menu:
            return {'message' :"No menu with given id."}
        args=update_menu_parser.parse_args()
        title=args.get('title')

        menu.title=title
        db.session.commit()

        return marshal(menu,menu_fields)
        

    def delete(self,id):
        menu=db.session.query(Menu).filter(Menu.id==id).first()
        if not menu:
            return {'message' :"No menu with given id."}
        db.session.delete(menu)
        db.session.commit()

        return {"message" :"Deleted"}
        # return marshal(menu,menu_fields)

    def post(self):
        all_menus=Menu.query.all()
        args=create_menu_parser.parse_args()
        title=args.get('title')
        menu_list=[menu.title for menu in all_menus]
        if title in menu_list:
            return {'message' :'This menu is already in the database'}
        if not title:
            raise BusinessValidationError(status_code=404 ,error_code=' ' ,error_message='Please enter a title for Menu')
        
        menu=Menu(title=title)
        db.session.add(menu)
        db.session.commit()

        return marshal(menu,menu_fields)
