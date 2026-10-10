from src import db
from flask_login import UserMixin




class Users(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(250),nullable=False)

class Uacs_object_code(db.Model):
    id=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(10),nullable=False)

class Items(db.Model):
    __tablename__="items"
    id=db.Column(db.String(10),primary_key=True)
    item_name=db.Column(db.String(250),unique=True,nullable=False)
    unit_cost=db.Column(db.Numeric(precision=6,scale=2),unique=False,nullable=False)
    unit_type=db.Column(db.String(10),nullable=False)
    uacs_code=db.Column(db.String(10))

    def all_items():
        return Items.query.order_by(Items.id).all()

class Transactions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    item_id=db.Column(db.String(10),db.ForeignKey("items.id"))
    items_used=db.Column(db.Integer,nullable=False)
    batch_no=db.Column(db.String(11))
    serial_no=db.Column(db.String(11))
    date_log=db.Column(db.Date,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    timestamp=db.Column(db.DateTime,nullable=False)
    users =db.relationship("Users")
    items=db.relationship("Items")