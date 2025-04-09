from flask_restful import Resource,reqparse,fields,marshal
import werkzeug
from application.validation import *
import cloudinary
from application.model import *

create_item_parser=reqparse.RequestParser()
create_item_parser.add_argument('menu_sub_id',location='form')
create_item_parser.add_argument('name',location='form')

create_item_parser.add_argument('image',type=werkzeug.datastructures.FileStorage, location='files')

update_item_parser=reqparse.RequestParser()
update_item_parser.add_argument('menu_sub_id',location='form')
update_item_parser.add_argument('name',location='form')

update_item_parser.add_argument('image',type=werkzeug.datastructures.FileStorage, location='files')

item_fields={
    'id' :fields.Integer,
    'menu_sub_id' :fields.Integer,
    'name':fields.String,
    'image':fields.String
}

class MenuItemAPI(Resource):
    def get(self,id=None):
        if id :
            menu_item=db.session.query(Menu_Items).filter(Menu_Items.id==id).first()
            return marshal(menu_item,item_fields)
        
        args=create_item_parser.parse_args()
        menu_sub_id=args.get('menu_sub_id')
        if menu_sub_id:
            sub=db.session.query(Menu_Items).filter(Menu_Items.menu_sub_id==menu_sub_id).all()
            return marshal(sub,item_fields)
        else:
            all_menu_item=Menu_Items.query.all()
            return marshal(all_menu_item,item_fields)
        

    def put(self,id):
        menu_item=db.session.query(Menu_Items).filter(Menu_Items.id==id).first()
        if not menu_item:
            raise NotFoundError(status_code=404)
        args=update_item_parser.parse_args()
        menu_sub_id=args.get('menu_sub_id')
        name=args.get('name')
        image=args.get('image')

        if menu_sub_id:
            menu_item.menu_sub_id=menu_sub_id
        if name:
            menu_item.name=name
        if image:
              # Extract the public id of current image url if exists
           if menu_item.image:
               public_id=menu_item.image.split('/')[-1].split('.')[0]

           result=cloudinary.uploader.upload(image,public_id=public_id,resource_type='image')
           new_image_url=result['secure_url']
        
           if new_image_url is None:
                raise BusinessValidationError(status_code=404,error_code='' ,error_message=' new image url  is required')
           
        db.session.commit()
        return marshal(menu_item,item_fields) 

    def delete(self,id):
        menu_item=db.session.query(Menu_Items).filter(Menu_Items.id==id).first()
        if not menu_item:
            raise NotFoundError(status_code=404)
        db.session.delete(menu_item)
        db.session.commit()

    def post(self):
        args=create_item_parser.parse_args()
        menu_sub_id=args.get('menu_sub_id')
        name=args.get('name')
        image=args.get('image')
        if not menu_sub_id:
            raise BusinessValidationError(status_code=404,error_code='',error_message='Menu sub id is required')
        if not name:
            raise BusinessValidationError(status_code=404,error_code='',error_message='name is required')
        if not image:
            raise BusinessValidationError(status_code=404,error_code='',error_message='image is required')
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(image,resource_type='image')

        # Get URL of uploaded image
        image_url = result['secure_url']

        if image_url is None:
            raise BusinessValidationError(status_code=404,error_code='' ,error_message='image url  is required')
        
        new_menu_item=Menu_Items(menu_sub_id=menu_sub_id,name=name,image=image_url)
        db.session.add(new_menu_item)
        db.session.commit()

        return marshal(new_menu_item,item_fields)