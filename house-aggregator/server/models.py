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
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    orders = db.relationship('Order', backref='User', lazy=True)
    balance = db.Column(db.Integer)

    def __repr__(self):

        return f'<User - Id: {self.id}, Name: {self.name}, Email: {self.email}, Orders: {list(self.orders)}>'

class Ticket(db.Model):
    """
    A ticket model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    date = db.Column(db.String(8)) # 20201104
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    orders = db.relationship('Order', backref='Ticket', lazy=True)

    def __repr__(self):

        return f'<Ticket - Name: {self.name}, Orders: {list(self.orders)}, Creator: {self.creator}>'

class Order(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f'<Order User - ID: {self.user_id}, Ticket ID: {self.ticket_id}, Quantity: {self.quantity}>'


# it creates all the SQL tables if they do not exist
with app.app_context():

    db.create_all()
    db.session.commit()