from flask import (
    Flask, 
    render_template, 
    request, 
    url_for, 
    redirect, 
    flash,
    jsonify, 
    session as login_session
)
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from new_database_setup import Base, Category, Game, User
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2, json, requests, cgi, random, string

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "Game Catalog App"

# Setting up database connections
engine = create_engine('sqlite:///gameshop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    # Render Login Template
    return render_template('login.html', STATE=state)


# Gconnect function to login via Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Function that establishes connection with Google when
    'Sign in using Google' button is selected.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorisation code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # exchange the access code for google creds
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get the access token from credentials and check that it is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
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
        response = make_response(json.dumps('User is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px; height: 300px; border-radius: 150px;
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> """
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    """
    This function revokes a current user's token and resets their
    login_session.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You have successfully been logged out!")
        return redirect(url_for("showCategory"))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

"""
Code for all API endpoints
"""


@app.route('/category/JSON')
def categoryJSON():
    """
    Making an API endpoint - for all categories
    """
    categories = session.query(Category).all()
    return jsonify(Game=[i.serialize for i in categories])


@app.route('/category/<int:category_id>/game/JSON')
def gamesInCategoryJSON(category_id):
    """
    Making an API endpoint - for all games in a category
    """
    category = session.query(Category).filter_by(id=category_id).one()
    games = session.query(Game).filter_by(category_id=category.id).all()
    return jsonify(Game=[i.serialize for i in games])


@app.route('/category/<int:category_id>/game/<int:game_id>/JSON')
def gameJSON(category_id, game_id):
    """
    Making an API endpoint - for details about a game
    """
    oneGame = session.query(Game).filter_by(
        category_id=category_id, id=game_id).one()
    return jsonify(Game=oneGame.serialize)


@app.route('/')
@app.route('/category/')
def showCategory():
    """
    This function shows all categories
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('publicCategory.html', categories=categories)
    return render_template('category.html', categories=categories)


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    """
    This function adds new category
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("New category created!")
        return redirect(url_for('showCategory'))
    else:
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    """
    This function edits an existing category
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editCategory = session.query(Category).filter_by(id=category_id).one()
    if editCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() "\
               "{alert('You are not authorised to access this page. " \
               "Please create your own category in order to edit');} " \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editCategory.name = request.form['name']
            session.add(editCategory)
            session.commit()
            flash("Category edited!")
            return redirect(url_for('showCategory'))
    else:
        return render_template('editCategory.html', category_id=category_id,
                               category=editCategory)


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """
    This function deletes an existing category
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteCategory = session.query(Category).filter_by(id=category_id).one()
    if deleteCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorised to access this page. " \
               "Please create your own category in order to delete');} " \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deleteCategory)
        session.commit()
        flash("Category deleted!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category_id=category_id,
                               category=deleteCategory)


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/game/')
def showGames(category_id):
    """
    This function shows all the games in a category
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    print category.user_id
    creator = getUserInfo(category.user_id)
    games = session.query(Game).filter_by(category_id=category.id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template('publicGame.html', category=category,
                               games=games, creator=creator)
    else:
        return render_template('game.html', category=category, games=games,
                               creator=creator)


@app.route('/category/<int:category_id>/game/new/', methods=['GET', 'POST'])
def newGame(category_id):
    """
    This function adds a game to a category
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to add games to this category." \
               " Please create your own category in order to add games.');}" \
               "</script><body onload='myFunction()'>"
    if request.method == 'POST':
        newGame = Game(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'], category_id=category_id,
                       user_id=login_session['user_id'])
        session.add(newGame)
        session.commit()
        flash("New game added!")
        return redirect(url_for('showGames', category_id=category_id))
    else:
        return render_template('newGame.html', category_id=category_id)


@app.route('/category/<int:category_id>/game/<int:game_id>/edit/',
           methods=['GET', 'POST'])
def editGame(category_id, game_id):
    """
    This function edits a game in a category
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editGame = session.query(Game).filter_by(id=game_id).one()
    if editGame.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorised to access this page. " \
               "Please create your game in order to edit');}</script>" \
               "<body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editGame.name = request.form['name']
        if request.form['description']:
            editGame.description = request.form['description']
        if request.form['price']:
            editGame.price = request.form['price']
        session.add(editGame)
        session.commit()
        flash("Game edited successfully!")
        return redirect(url_for('showGames', category_id=category_id))
    else:
        return render_template('editGame.html', category_id=category_id,
                               game=editGame)


@app.route('/category/<int:category_id>/game/<int:game_id>/delete/',
           methods=['GET', 'POST'])
def deleteGame(category_id, game_id):
    """
    This function deletes a game from a category
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    delGame = session.query(Game).filter_by(id=game_id).one()
    if delGame.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorised to access this page. " \
               "Please create your game in order to delete');}</script>" \
               "<body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(delGame)
        session.commit()
        flash("Game deleted successfully!")
        return redirect(url_for('showGames', category_id=category_id))
    else:
        return render_template('deleteGame.html', category_id=category_id,
                               game=delGame)

if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
