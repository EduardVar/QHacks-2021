from werkzeug.security import generate_password_hash, check_password_hash

from datetime import date, datetime
from typing import List, Union, Optional
import re

"""
This file defines all backend logic that interacts with database and other services
"""

def validate_email(email : str):

    # RFC 5322 specification: https://emailregex.com/
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.search(regex, email)

def validate_name(name):

    if 2 > len(name) > 20: return "Username must be between 2 and 20 characters."
    if not name.isalnum(): return "Name must be alphanumeric only."

    return None

def validate_password(password : str):

    pkg = {'state': True, 'msg': ''}

    regex = r"(^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$)"
    if len(password) < 6: 
        pkg['state'] = False
        pkg['msg'] = "Password length must be greator then 6."
    elif re.search(regex, password) == None:
        pkg['state'] = False
        pkg['msg'] = "You password must meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character (@$!%*?&)"

    return pkg

def get_user(email : str) -> Optional[User]:
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user

def add_user_funds(email : str, amount) -> None:

    user = get_user(email)
    user.balance += amount
    db.session.commit()

def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    :return: message "email/password combination incorrect" if login fails
    """
    # if this returns a user, then the name already exists in database

    email = email.strip()
    password = password.strip()

    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user

def register_user(email : str, name : str, password : str, password2 : str):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """
    email = email.strip()
    name = name.strip().lower()
    password = password.strip()
    password2 = password2.strip()

    user = User.query.filter_by(email=email).first()

    if user:
        return "This email is already in use."

    name_validation_error = validate_name(name)
    if not name_validation_error == None:
        return name_validation_error

    password_validation_error = validate_password(password)

    if not password_validation_error['state']:
        return password_validation_error['msg']

    if password != password2:
        return "The passwords do not match."

    if not validate_email(email):
        return 'Invalid Email.'

    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw, balance=5000)

    db.session.add(new_user)
    db.session.commit()
    return None

def get_available_tickets(user : User = None) -> List[Ticket]:

    if (user):
        return Ticket.query.filter_by(creator=user.id)
    return Ticket.query.all()

def check_if_expired(ticket : Ticket) -> bool:

    return ticket.date <= date.today().strftime("%Y%m%d")

def validate_ticket_inputs(name, price, day : str, amount, user):

    if not bool(re.search(r'^[A-Za-z0-9 ]*$', name)):
        return "Name must be alphanumeric"

    if not (len(name) in range(6, 61)):
        return "Name length must be between 6 and 60 characters"

    if datetime.strptime(day, '%Y%m%d').date() < date.today():
        return "This ticket has expired"

    if not (amount in range(1, 101)):
        return "Please select 1 to 100 tickets"

    return None

def buy_ticket(name : str, price : float, day : str, amount : int, user : User) -> Union[str, None]:

    errors = validate_ticket_inputs(name, price, day, amount, user)
    if (errors != None): return errors

    price *= amount
    price += (price * 0.35) + (price * 0.05)

    print(f'User Balance: {user.balance}')
    print(f'Ticket Price: {price}')

    if user.balance < price:
        return "You do not have enough funds to purchase this"

    ticket = Ticket.query.filter_by(name=name).filter_by(date=day).first()

    if (ticket == None):
        return "The requested ticket was not found"

    if (ticket.quantity < amount):
        return "There are not enough tickets available"

    ticket.quantity -= amount
    user.balance -= price
    order = Order(user_id=user.id, ticket_id=ticket.id, quantity=amount)

    db.session.add(order)
    db.session.commit()

def sell_ticket(name : str, price : float, day : str, amount : int, user : User) -> Union[str, None]:

    errors = validate_ticket_inputs(name, price, day, amount, user)

    if (errors != None): return errors

    if not (price in range(10, 101)):
        return "Please enter an amount between 10 and 100"

    if (Ticket.query.filter_by(name=name).filter_by(date=day).first() != None):
        return "There is a ticket already specified"

    ticket = Ticket(name=name, price=price, date=day, creator=user.id, quantity=amount)

    db.session.add(ticket)
    db.session.commit()

def update_ticket(name : str, price : str, day : str, amount : str, user : User, ticket_id : int) -> Union[str, None]:

    errors = validate_ticket_inputs(name, price, day, amount, user)

    if (errors != None): return errors

    if not (price in range(10, 101)):
        return "Please enter an amount between 10 and 100"

    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if (ticket == None):
        return "The requested ticket was not found"

    ticket.name = name
    ticket.price = price
    ticket.quantity = amount
    ticket.date = day.replace("/", "")

    db.session.commit()

def clean_database():
    db.session.query(Ticket).delete()
    db.session.commit()
