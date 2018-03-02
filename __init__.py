from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from flask import session as login_session
import random, string
from werkzeug import secure_filename
import os

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# database initialization
engine = create_engine('postgresql://catalog1:db-password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
CLIENT_ID = json.loads(open(''/var/www/udacity-FSD/client_secrets.json'',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"
UPLOAD_FOLDER = './static/Restaurants'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# generate alpha-numeric string for CSRF token
def generate_csrf_token():
    if '_csrf_token' not in login_session:
        login_session['_csrf_token'] = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for x in xrange(32))
    return login_session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


#region login_through_google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_Id = getUserID(data['email'])
    if user_Id is None:
        user_Id = createUser()
    login_session['user_Id'] = user_Id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
#endregion login_through_google

#region log_out
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully disconnected.')
        return redirect(url_for('showRestaurants'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
#endregion


# User Helper Functions

def createUser():
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        pass

# Restaurant-CRUD
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurant_list = session.query(Restaurant).all()
    if 'username' not in login_session:
        return render_template('publicRestaurant.html', restaurantList=restaurant_list)
    else:
        return render_template('restaurants.html', restaurantList=restaurant_list)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurants():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return "Forbidden"
        new_restaurant = Restaurant()
        new_restaurant.name = request.form['name']
        new_restaurant.user_id = login_session['user_Id']
        file_read = request.files['file']
        # upload file at specified folder
        if file_read:
            filename = secure_filename(file_read.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_read.save(file_path)
            new_restaurant.picture = file_path
        session.add(new_restaurant)
        session.commit()
        flash("Inserted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurants(restaurant_id):
    restaurant_details = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    creator = getUserInfo(restaurant_details.user_id)
    if 'username' not in login_session or creator.id != login_session['user_Id']:
        flash("You are not the owner")
        return redirect(url_for('showRestaurants'))
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return "Forbidden"
        restaurant_details.name = request.form['name']
        session.add(restaurant_details)
        session.commit()
        flash("Updated")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editRestaurant.html', restaurant=restaurant_details)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurants(restaurant_id):
    restaurant_details = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    creator = getUserInfo(restaurant_details.user_id)
    if 'username' not in login_session or creator.id != login_session['user_Id']:
        flash("You are not the owner")
        return redirect(url_for('showRestaurants'))
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return "Forbidden"
        session.delete(restaurant_details)
        session.commit()
        flash("Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'deleteRestaurant.html', restaurant=restaurant_details)

# All Restaurants json
@app.route('/restaurants/JSON')
def showRestaurantsJson():
    if 'username' not in login_session:
        return "Error: Not authorized"
    restaurant = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurant])


# Menu-CRUD
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant_menu_list = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    restaurant_details = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    creator = getUserInfo(restaurant_details.user_id)
    if creator is None or 'username' not in login_session or creator.id != login_session['user_Id']:
        return render_template(
            'publicMenuItem.html',
            menuList=restaurant_menu_list,
            restaurant_id=restaurant_id,
            restaurant_name=restaurant_details.name)
    else:
        return render_template(
            'menu.html',
            menuList=restaurant_menu_list,
            restaurant_id=restaurant_id,
            restaurant_name=restaurant_details.name)


@app.route(
    '/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit',
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return "Forbidden"
        menu_item.name = request.form['name']
        menu_item.price = request.form['price']
        menu_item.course = request.form['course']
        menu_item.description = request.form['description']
        session.add(menu_item)
        session.commit()
        flash("Updated")
        return redirect(
            url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', menuItem=menu_item)


@app.route(
    '/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete',
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return "Forbidden"
        session.delete(menu_item)
        session.commit()
        flash("Deleted")
        return redirect(
            url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', menuItem=menu_item)


@app.route(
    '/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def addNewMenuItem(restaurant_id):
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return "Forbidden"
        menu_item = MenuItem()
        menu_item.name = request.form['name']
        menu_item.price = request.form['price']
        menu_item.course = request.form['course']
        menu_item.description = request.form['description']
        menu_item.restaurant_id = restaurant_id
        menu_item.user_id = login_session['user_Id']
        session.add(menu_item)
        session.commit()
        flash("Inserted")
        return redirect(
            url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

# Retruns json for all menus of perticular restaurants
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def showMenuJson(restaurant_id):
    if 'username' not in login_session:
        return "Error: Not authorized"
    restaurant_menu_list = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(
        restaurant_menu_list=[i.serialize for i in restaurant_menu_list])

# Retruns json for specific menu
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showSingleMenuJson(restaurant_id, menu_id):
    if 'username' not in login_session:
        return "Error: Not authorized"
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menu_item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

