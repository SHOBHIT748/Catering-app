import cloudinary.uploader
from flask_restful import Resource,fields,marshal,reqparse
import werkzeug
from application.validation import *
from application.model import *
import cloudinary

create_gallery_parser=reqparse.RequestParser()
create_gallery_parser.add_argument('image',type=werkzeug.datastructures.FileStorage, location='files')

gallery_fields={
    'id':fields.Integer,
    'image':fields.String
}

class galleryAPI(Resource):
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
