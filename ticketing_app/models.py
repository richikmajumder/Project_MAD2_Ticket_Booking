from flask_sqlalchemy import SQLAlchemy
from flask_login import *

db = SQLAlchemy()


class Venue(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(), nullable=False)
  place = db.Column(db.String(), nullable=False)
  location = db.Column(db.String(), nullable=False)
  capacity = db.Column(db.Integer, nullable=False)
  link = db.relationship("Link", backref="venue", cascade="all,delete")
  booking = db.relationship("Booking", backref="venue", cascade="all,delete")


class Show(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(), unique=True, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  tags = db.Column(db.String(), nullable=False)
  link = db.relationship("Link", backref="show", cascade="all,delete")
  booking = db.relationship("Booking", backref="show", cascade="all,delete")
  ratings = db.relationship("Rating",backref="show",cascade="all,delete")


class Link(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
  show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
  date = db.Column(db.Date(), nullable=False)
  time = db.Column(db.Time(), nullable=False)
  ticket_price = db.Column(db.Integer, nullable=False)
  tickets_left = db.Column(db.Integer, nullable=False)
  booking = db.relationship("Booking",backref="link",cascade="all,delete")


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(), nullable=False, unique=True)
  email = db.Column(db.String(), nullable=False, unique=True)
  firstname = db.Column(db.String(), nullable=False)
  lastname = db.Column(db.String(), nullable=False)
  wallet = db.Column(db.Integer)
  pdf_report = db.Column(db.Integer)
  password = db.Column(db.String(), nullable=False)
  is_admin = db.Column(db.Boolean(), default=False)
  last_login = db.Column(db.DateTime())
  booking = db.relationship("Booking", backref="user", cascade="all,delete")
  token = db.relationship("PasswordResetToken", backref="user", cascade="all,delete")


class Booking(db.Model):
  id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
  link_id = db.Column(db.Integer, db.ForeignKey("link.id"), nullable=False)
  tickets_booked = db.Column(db.Integer, nullable=False)
  ticket_price = db.Column(db.Integer, nullable=False)
  date = db.Column(db.Date, nullable=False)


class Rating(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
  rating = db.Column(db.Integer, nullable=False)


class PasswordResetToken(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  token = db.Column(db.String, unique=True, nullable=False)
  validity = db.Column(db.DateTime(),nullable=False)

'''with app.app_context():
  db.create_all()'''
