from .database import db
from flask_login import UserMixin
from datetime import datetime


# Create user model
class Users(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    email= db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role=db.Column(db.String(20),default='user')

class Services(db.Model):
    __tablename__='service'
    id= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30),nullable=False)
    description=db.Column(db.String(1000))
    image=db.Column(db.String,nullable=False)  # URL will be given here,not the exact images.


class Menu(db.Model):
    __tablename__='menu'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(30),nullable=False)


class Menu_Sub(db.Model):
    __tablename__='menu_sub'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(30),nullable=False)

    menu_id=db.Column(db.Integer,db.ForeignKey('menu.id'),nullable=False)

class Menu_Items(db.Model):
    __tablename__='menu_items'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)

    image=db.Column(db.String,nullable=False)
    menu_sub_id=db.Column(db.Integer,db.ForeignKey('menu_items.id'),nullable=False)


class Gallery(db.Model):
    __tablename__='gallery'
    id=db.Column(db.Integer,primary_key=True)
    image=db.Column(db.String,nullable=False)

class Contact(db.Model):
    __tablename__='contact'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    phone_number=db.Column(db.Integer,nullable=False)
    query=db.Column(db.String(500),nullable=False)

class Testimonial(db.Model):
    __tablename__='testimonial'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=True)

class Booking(db.Model):
    __tablename__='booking'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String,nullable=False)
    occasion=db.Column(db.String )
    dishes=db.Column(db.String,nullable=False)
    no_of_person=db.Column(db.Integer,nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Stores date + time
    message=db.Column(db.String(300))

class Checkout(db.Model):
    __tablename__='checkout'
    id=db.Column(db.Integer,primary_key=True)
    cartitems=db.Column(db.JSON)
    userinfo=db.Column(db.JSON)
    total_dishes=db.Column(db.Integer)
    total_persons=db.Column(db.Integer)



