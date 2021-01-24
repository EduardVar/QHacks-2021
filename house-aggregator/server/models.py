from server import app
from flask_sqlalchemy import SQLAlchemy

"""
This file defines all models used by the server
These models provide us a object-oriented access
to the underlying database, so we don't need to 
write SQL queries such as 'select', 'update' etc.
"""

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    """
    A user model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    bookmarks = db.Column(db.String(10000))

class House(db.Model):
    """
    A Housing model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.String(100))
    address = db.Column(db.String(500))
    #bedrooms = db.Column(db.Float)
    #bathrooms = db.Column(db.Float)
    description = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    #landlord = db.Column(db.String(100))
    date = db.Column(db.String(100)) # 20201104
    img_urls = db.Column(db.String(1000))

# it creates all the SQL tables if they do not exist
with app.app_context():

    db.create_all()
    db.session.commit()
