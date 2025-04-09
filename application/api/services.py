import cloudinary.uploader
from flask_restful import Resource,reqparse,fields,marshal_with,marshal
from flask import request ,jsonify 
from application.validation import BusinessValidationError
import cloudinary
from cloudinary import uploader
from application.model import *
import werkzeug

create_service_parser=reqparse.RequestParser()
create_service_parser.add_argument('title',location='form')
create_service_parser.add_argument('description',location='form')
# If you are uploading an actual file, use:
create_service_parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

update_service_parser=reqparse.RequestParser()
update_service_parser.add_argument('title',location='form')
update_service_parser.add_argument('description',location='form')
# If you are uploading an actual file, use:
update_service_parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')





service_fields={
    'title' : fields.String ,
    'description' :fields.String,
    'image' :fields.String
}

class ServicesAPI(Resource):
    @marshal_with(service_fields)
    def get(self,id=None):
        if id :
            service=db.session.query(Services).filter(Services.id==id).first()
            if not service :
                raise BusinessValidationError(status_code=404 ,error_code='' ,error_message='No service with given id .')
            
            return service
        else:
            all_services=Services.query.all()
            # List of serialized objects
            return  [marshal(service, service_fields) for service in all_services]  
    
    @marshal_with(service_fields)
    def put(self,id):
        service=db.session.query(Services).filter(Services.id==id).first()
        if not service:
             raise BusinessValidationError(status_code=404,error_code='' ,error_message='no such service ')
        
        args=update_service_parser.parse_args()
        title=args.get('title')
        description=args.get('description')
        image=args.get('image')

        if title:
            service.title=title
        if description:
            service.description=description
        if image:
            # Extract the public id of current image url if exists
           if service.image:
               public_id=service.image.split('/')[-1].split('.')[0]

           result=cloudinary.uploader.upload(image,public_id=public_id,resource_type='image')
           new_image_url=result['secure_url']
        
           if new_image_url is None:
                raise BusinessValidationError(status_code=404,error_code='' ,error_message=' new image url  is required')
        
        db.session.commit()
        return service
        

    def delete(self,id):
        service=db.session.query(Services).filter(Services.id==id).first()
        if not service:
             raise BusinessValidationError(status_code=404,error_code='' ,error_message='no such service ')
        
        if service.image:
               public_id=service.image.split('/')[-1].split('.')[0]
        
        result=cloudinary.uploader.destroy(public_id=public_id)
        

        
        db.session.delete(service)
        db.session.commit()
        return {'message': "deleted successfully"}

    def post(self):
        print(0)
        args=create_service_parser.parse_args()
        print(1)
        title=args.get('title')
        description=args.get('description')
        # image=request.get('image')
        # if 'image' not in args.files:
        #    return jsonify({"error": "No image file provided"}), 400
        print(2)
        image = args.get('image')
        print(3)


        if title is None:
            raise BusinessValidationError(status_code=404,error_code='' ,error_message='Title is required')
        
        if description is None:
            raise BusinessValidationError(status_code=404,error_code='' ,error_message='Description is required')
        
        if image is None:
            raise BusinessValidationError(status_code=404,error_code='' ,error_message='image  is required')
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(image,resource_type='image')

        # Get URL of uploaded image
        image_url = result['secure_url']

        if image_url is None:
            raise BusinessValidationError(status_code=404,error_code='' ,error_message='image url  is required')
        
        service=Services(title=title,description=description,image=image_url)
        db.session.add(service)
        db.session.commit()

        return marshal(service,service_fields)

       
        


