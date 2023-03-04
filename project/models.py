from sqlalchemy.orm import relationship
from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    # __tablename__ = "users" # crées le nom de ma table
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000), unique=True)
    # lastname=db.column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    missions = relationship("Mission", backref="poster", lazy='dynamic')

    # creat a function to return the a string when add something
    def __repr__(self):
        return f"{self.id}, {self.username}"


class Mission(db.Model):
    # __tablename__ = "Aides" # crées le nom de ma table
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    id_ex_user = db.Column(db.Integer, db.ForeignKey(
        'user.id'))  # ,unique=True, on as pas le upper dans users car c'est comme qu'il secris sur le databse
    mission = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(200))

    # creat a function to return the a string when add something
    def __repr__(self):
        return f"{self.mission}"
    ### function importante pour la lecture string
