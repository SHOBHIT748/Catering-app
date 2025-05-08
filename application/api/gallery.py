import cloudinary.uploader
from flask_restful import Resource,fields,marshal,reqparse
from sqlalchemy import desc
import werkzeug
from application.validation import *
from application.model import *
import cloudinary
# from cloudinary import config
# print(config().cloud_name, config().api_key, config().api_secret)

create_gallery_parser=reqparse.RequestParser()
create_gallery_parser.add_argument('image',type=werkzeug.datastructures.FileStorage, location='files')

gallery_fields={
    'id':fields.Integer,
    'image':fields.String
}

class galleryAPI(Resource):
    def get(self,id=None):
         if id :
            gallery=db.session.query(Gallery).filter(Gallery.id==id).first()
            if not gallery :
                raise BusinessValidationError(status_code=404 ,error_code='' ,error_message='No gallery image with given id .')

            return marshal(gallery,gallery_fields)
         else:
            all_gallery=Gallery.query.order_by(desc(Gallery.id)).all()
            # List of serialized objects
            return  [marshal(gallery, gallery_fields) for gallery in all_gallery]

    def delete(self,id):
        gallery=db.session.query(Gallery).filter(Gallery.id==id).first()
        if not gallery:
            raise BusinessValidationError(status_code=404 ,error_code='' ,error_message='No such image')
        db.session.delete(gallery)
        db.session.commit()
        return {'message':'deleted successfully'}

    def post(self):
        args=create_gallery_parser.parse_args()
        image=args.image
        if not image:
            raise BusinessValidationError(status_code=404,error_code=' ',error_message='image is required')

        result=cloudinary.uploader.upload(image)

        image_url=result['secure_url']

        if not image_url:
            raise BusinessValidationError(status_code=404,error_code=' ',error_message='image url is required')

        gallery=Gallery(image=image_url)
        db.session.add(gallery)
        db.session.commit()

        return marshal(gallery,gallery_fields)

