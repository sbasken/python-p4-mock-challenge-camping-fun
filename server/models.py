from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })


db = SQLAlchemy()

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-created_at', '-updated_at','-campers.activities', '-signups.activity')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', backref='activity')
    activities = association_proxy('signups', 'activity')

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ('-created_at', '-updated_at', '-activity.signups', '-camper.signups')

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('time')
    def validates_name(self, key, time):
        if not 0 <= time <= 23:
            raise ValueError('time must be 0 and 23')
        return time

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-created_at', '-updated_at', '-activities.campers', '-signups.camper')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint( 'age >= 18'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', backref='camper')
    activities = association_proxy('signups', 'activity')

    __table_args__ = (
        db.CheckConstraint( 'age >= 18' ), 
    )

    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError('Camper must have a name')
        return name
    
    @validates('age')
    def validates_name(self, key, age):
        if not 8 <= age <= 18:
            raise ValueError('Age must be between 8 and 18.')
        return age

# add any models you may need. 