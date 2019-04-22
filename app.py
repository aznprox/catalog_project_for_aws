from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Make, Model, User

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Car Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///carmake.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


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
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
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
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'
    for allinfo in login_session:
        print allinfo
    
    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

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


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.2/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v3.2/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v3.2/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"
    
# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
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
        return None


#------------------
#JSON API ENDPOINTS
#------------------

@app.route('/makes/JSON')
def showMakesJSON():
    makes = session.query(Make).all()
    return jsonify(AllMakes=[m.serialize for m in makes])

@app.route('/makes/<int:make_id>/JSON')
def showOneMakeJSON(make_id):
    oneMake = session.query(Make).filter_by(id=make_id).one()
    return jsonify(Make=[oneMake.serialize])

@app.route('/make/<int:make_id>/model/JSON')
def showMakeModelsJSON(make_id):
    models = session.query(Model).filter_by(make_id=make_id).all()
    return jsonify(AllModels=[m.serialize for m in models])

@app.route('/make/<int:make_id>/model/<int:model_id>/JSON')
def showOneModelJSON(make_id, model_id):
    model = session.query(Model).filter_by(id=model_id).one()
    return jsonify(oneModel=model.serialize)

#--------------------
#CRUD FUNCTIONALITIES
#--------------------

#Home/Root routing to show all car makes
@app.route('/')
@app.route('/makes')
def showMakeMenu():
    makes = session.query(Make).all()
    if 'username' not in login_session:
        return render_template('makes.html', makes = makes)
    else:
        latestModels = session.query(Model).order_by(Model.id.desc())[0:3]
        return render_template('latestCars.html', makes = makes, models = latestModels)

#Create a new automobile make
@app.route('/makes/new', methods=['GET', 'POST'])
def newMake():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newMake = Make(
        user_id=login_session['user_id'],
        name=request.form['name'], 
        image=request.form['image'],
        description=request.form['description'])
     
        session.add(newMake)
        session.commit()
        flash("NEW MAKE ADDED!")
        return redirect(url_for('showMakeMenu'))
    else:
        return render_template('newMake.html')

#Edit an existing car make
@app.route('/makes/<int:make_id>/edit', methods=['GET', 'POST'])
def editMake(make_id):
    editedMake = session.query(Make).filter_by(id=make_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedMake.user_id != login_session['user_id']:
        flash("You are not authroized to edit this")
        return redirect(url_for('showMakeMenu'))  
    if request.method =='POST':
        if request.form['name']:
            editedMake.name = request.form['name']
        if request.form['image']:
            editedMake.image = request.form['image']
        if request.form['description']:
            editedMake.description = request.form['description']
        session.add(editedMake)
        session.commit()
        flash("A MAKE WAS EDITED!")
        return redirect(url_for('showMakeMenu'))
    else:
        return render_template('editMake.html', make_id=make_id, beingEditedMake = editedMake)

#Delete an existing car make
@app.route('/makes/<int:make_id>/delete', methods=['GET', 'POST'])
def deleteMake(make_id):
    makeToDelete = session.query(Make).filter_by(id=make_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if makeToDelete.user_id != login_session['user_id']:
        flash("You are not authroized to delete this")
        return redirect(url_for('showMakeMenu'))       
    if request.method == 'POST':
        session.delete(makeToDelete)
        session.commit()
        flash("A MAKE WAS DELETED!")
        return redirect(url_for('showMakeMenu'))
    else:
        return render_template('deleteMake.html', make = makeToDelete)
    
#Show all the models of a specific make
@app.route('/make/<int:make_id>/')
@app.route('/make/<int:make_id>/model')
def showMakeModels(make_id):
    make = session.query(Make).filter_by(id=make_id).one()
    models = session.query(Model).filter_by(make_id=make_id)
    return render_template('selections.html', make_id = make_id, models=models, make=make)

#Show information of a specific make/model
@app.route('/make/<int:make_id>/model/<int:model_id>/')
def showMakeModelOne(make_id, model_id):
    oneModel = session.query(Model).filter_by(id=model_id)
    return render_template('oneModel.html', make_id = make_id, models=oneModel)

#Add a new model based on make_id
@app.route('/make/<int:make_id>/model/new', methods=['GET', 'POST'])
def addMakeModels(make_id):
    if 'username' not in login_session:
        return redirect('/login')
    make = session.query(Make).filter_by(id=make_id).one()
    if make.user_id != login_session['user_id']:
        flash("You are not authroized to add a new model to this make")
        return redirect(url_for('showMakeModels', make_id = make_id)) 
    if request.method == 'POST':
        newModel = Model(
            user_id=login_session['user_id'],
            name=request.form['name'],
            image=request.form['image'],
            description=request.form['description'],
            price=request.form['price'],
            make_id=make_id
        )
        session.add(newModel)
        session.commit()
        flash("A NEW MODEL WAS ADDED!")
        return redirect(url_for('showMakeModels', make_id = make_id))
    else:
        return render_template('newModel.html', make_id = make_id)

#Edit an existing model based on model_id
@app.route('/make/<int:make_id>/model/<int:model_id>/edit', methods =['GET', 'POST'])
def editMakeModels(make_id, model_id):
    editedModel = session.query(Model).filter_by(id=model_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedModel.user_id != login_session['user_id']:
        flash("You are not authroized to edit this")
        return redirect(url_for('showMakeModels', make_id = make_id))  
    if request.method == 'POST':
        if request.form['name']:
            editedModel.name = request.form['name']
        if request.form['description']:
            editedModel.description = request.form['name']
        if request.form['price']:
            editedModel.price = request.form['price']
        if request.form['image']:
            editedModel.image = request.form['image']
        session.add(editedModel)
        session.commit()
        flash("A MODEL WAS EDITIED!")
        return redirect(url_for('showMakeModels', make_id = make_id))
    else:
        return render_template('editModel.html',make_id=make_id, model_id = model_id, model = editedModel)

#Delete an existing model based on model_id
@app.route('/make/<int:make_id>/model/<int:model_id>/delete', methods =['GET', 'POST'])
def deleteMakeModels(make_id, model_id):
    deleteModel = session.query(Model).filter_by(id=model_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deleteModel.user_id != login_session['user_id']:
        flash("You are not authroized to delete this")
        return redirect(url_for('showMakeModels', make_id = make_id))
    if request.method == 'POST':
        session.delete(deleteModel)
        session.commit()
        flash("A MODEL WAS DELETED!")
        return redirect(url_for('showMakeModels', make_id = make_id))
    else:
        return render_template('deleteModel.html', model = deleteModel)

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showMakeMenu'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showMakeMenu'))

#Tells app to run on localhost:8000
if __name__ == '__main__':
    app.secret_key = 'super-secret-key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)