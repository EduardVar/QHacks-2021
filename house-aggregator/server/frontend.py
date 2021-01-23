from flask import render_template, request, session, redirect, flash
from server import app
import server.backend as bn
import random
from server.models import Ticket

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""

def get_error_message():
    session.get('error_message')
    return session.pop('error_message', None)

@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')

@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = bn.register_user(email, name, password, password2)
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        session['error_message'] = error_message
    
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login_get():

    if not session.get("error_message") is None:
        message = get_error_message()
    else:
        message = "Please Login"

    return render_template('login.html', message=message)

@app.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    user = bn.login_user(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be passed
        along between every request the browser made to this services.

        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.

        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/login')

def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner

@app.route('/', methods=['GET'])
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.

    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    if not session.get("error_message") is None:
        m = get_error_message()
    else:
        m = ''

    return render_template('index.html', user=user, tickets=bn.get_available_tickets(), msg=m)

@app.route('/*')
@app.errorhandler(404)
def page_not_found(message):
    #List of funny 404 messages
    messages = ["Seat's taken."
        , "You just lost musical chairs."
        , "Sorry, we're full"
        , "You don't have a ticket for this seat."
        , "Hey, that's my seat!"
        , "No loitering, get outta here."
        , "Please remain seated during takeoff and landing."
        , "You can't sit with us."]

    #Pick one of the messages at random

    return render_template("404.html", message=messages[random.randrange(len(messages))])
  
@app.route('/viewPOST', methods=['POST'])
def view(): 

    print(request.form.to_dict())
    return ('', 204)

@app.route('/buy', methods=['POST'], endpoint='buy_ticket')
@authenticate
def buy_ticket(user): 

    name = request.form.get('Name').strip()
    price = float(request.form.get('Price'))
    date = request.form.get('Date').replace("/", "")
    quantity = int(request.form.get('Quantity'))

    error_message = bn.buy_ticket(name, price, date, quantity, user)

    if error_message:
        session['error_message'] = error_message
        return render_template('index.html', user=user, tickets=bn.get_available_tickets(), msg=error_message)

    # Any response will have the webpage reload itself.
    return ('', 200)
    

@app.route('/update', methods=['POST'], endpoint="update_ticket")
@authenticate
def update_ticket(user): 

    name = request.form.get('Name').strip()
    price = float(request.form.get('Price'))
    date = request.form.get('Date').replace("/", "")
    quantity = int(request.form.get('Quantity'))
    ticket_id = int(request.form.get("Ticket_Id"))

    error_message = bn.update_ticket(name, price, date, quantity, user, ticket_id)

    if error_message:
        session['error_message'] = error_message
        return ('', 400)

    # Any response will have the webpage reload itself.
    return ('', 200)

@app.route('/sell', methods=['POST'], endpoint="sell_ticket")
@authenticate
def sell_ticket(user): 

    name = request.form.get('Name').strip()
    price = float(request.form.get('Price'))
    date = request.form.get('Date').replace("/", "")
    quantity = int(request.form.get('Quantity'))

    error_message = bn.sell_ticket(name, price, date, quantity, user)

    if error_message:
        session['error_message'] = error_message
        return render_template('index.html', user=user, tickets=bn.get_available_tickets(), msg=error_message)

    # Any response will have the webpage reload itself.
    return ('', 200)
    