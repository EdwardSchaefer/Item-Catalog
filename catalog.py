import os #for file uploads
import shutil #for file uploads
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Guitar, User
from werkzeug.utils import secure_filename

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['png'])
CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

engine = create_engine('sqlite:///guitars.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create a state token to prevent request forgery
#Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

#Connects a user with Facebook login
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

    #Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    #Strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    #The token must be stored in the login_session in order to properly logout,
    #let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    #See if user exists, if it doesn't, make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    return output

#Disconnect a user who is connected via Facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    #The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

#Connects a user with their Google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    #Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Obtain authorization code
    code = request.data

    try:
        #Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    #If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    #Add provider to login session
    login_session['provider'] = 'google'

    #See if user exists, if it doesn't, make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    print "done!"
    return output

#Disconnect a user who is connected with Google
@app.route('/gdisconnect')
def gdisconnect():
    #Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        #For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

#Disconnect based on provider
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
        del login_session['user_id']
        del login_session['provider']
        return redirect(url_for('showBrands'))
    else:
        return redirect(url_for('showBrands'))

#Create a new user
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

#Returns 'user' with user info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

#Gets the users ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

#Determines if a file to be uploaded is valid
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Returns JSON object of guitars from a brand with specifications
@app.route('/brand/<int:brand_id>/guitar/JSON')
def brandGuitarJSON(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    guitars = session.query(Guitar).filter_by(
        brand_id=brand_id).all()
    return jsonify(Guitar=[i.serialize for i in guitars])

#Returns a JSON object of a guitar and it's specifications
@app.route('/brand/<int:brand_id>/guitar/<int:guitar_id>/JSON')
def menuItemJSON(brand_id, guitar_id):
    Guitar = session.query(Guitar).filter_by(id=guitar_id).one()
    return jsonify(Guitar=Guitar.serialize)

#Returns a JSON object of brands
@app.route('/brand/JSON')
def brandsJSON():
    brands = session.query(Brand).all()
    return jsonify(brands=[b.serialize for b in brands])


#Show all brands
@app.route('/')
@app.route('/brand/')
def showBrands():
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    return render_template('brands.html', brands=brands,
                           user_id=user_id, username=username,
                           user=user)

#Create a new brand
@app.route('/brand/new/', methods=['GET', 'POST'])
def newBrand():
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBrand = Brand(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newBrand)
        session.commit()
        return redirect(url_for('showBrands'))
    else:
        return render_template('newBrand.html', brands=brands, user=user,
                               username=username, user_id=user_id)

#Edit a brand
@app.route('/brand/<int:brand_id>/edit/', methods=['GET', 'POST'])
def editBrand(brand_id):
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    editedBrand = session.query(
        Brand).filter_by(id=brand_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedBrand.name = request.form['name']
            return redirect(url_for('showBrands'))
    else:
        return render_template('editBrand.html', brand=editedBrand, brands=brands,
                               user=user, username=username, user_id=user_id)

#Upload a brand logo
@app.route('/brand/<int:brand_id>/logoImgUpload/', methods=['GET', 'POST'])
def logoImgUpload(brand_id):
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            brand_id_str = str(brand_id)
            filename = 'logos/' + brand_id_str + '.png'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('showBrands'))
    else:
        return render_template('ImgUpload.html', brand_id=brand_id, brands=brands,
                               user=user, username=username, user_id=user_id)

#Upload an image of a guitar
@app.route('/brand/<int:brand_id>/guitar/<int:guitar_id>/guitarImgUpload/',
           methods=['GET', 'POST'])
def guitarImgUpload(brand_id, guitar_id):
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            guitar_id_str = str(guitar_id)
            brand_id_str = str(brand_id)
            filename = brand_id_str + '/' + guitar_id_str + '.png'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            directory = os.path.dirname(file_path)
            #Check to see if the directory exists, and if it does not, create it
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(file_path)
            return redirect(url_for('showBrands'))
    else:
        return render_template('ImgUpload.html', brand_id=brand_id, guitar_id=guitar_id,
                               user_id=user_id, username=username, brands=brands, user=user)

#Show a brand's selection of guitars
@app.route('/brand/<int:brand_id>/')
@app.route('/brand/<int:brand_id>/guitars/')
def showGuitars(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    brands = session.query(Brand).all()
    guitars = session.query(Guitar).filter_by(brand_id=brand_id).all()
    return render_template('guitars.html', guitars=guitars, brand=brand,
                           brands=brands, username=username, user_id=user_id)

#Create a new guitar
@app.route(
    '/brand/<int:brand_id>/guitar/new/', methods=['GET', 'POST'])
def newGuitar(brand_id):
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    brand = session.query(Brand).filter_by(id=brand_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif login_session['user_id'] != brand.user_id:
        return redirect(url_for('showBrands'))
    elif request.method == 'POST':
        newGuitar = Guitar(name=request.form['name'],
                           body_material=request.form['body_material'],
                           neck_material=request.form['neck_material'],
                           fingerboard_material=request.form['fingerboard_material'],
                           frets=request.form['frets'],
                           strings=request.form['strings'],
                           scale_length=request.form['scale_length'],
                           pickups=request.form['pickups'],
                           bridge=request.form['bridge'],
                           brand_id=brand_id,
                           user_id=brand.user_id)
        session.add(newGuitar)
        session.commit()
        return redirect(url_for('showGuitars', brand_id=brand_id))
    else:
        return render_template('newGuitar.html', brand_id=brand_id, brands=brands, user=user,
                               username=username, user_id=user_id)
    return render_template('newGuitar.html', brand=brand)

#Edit a guitar
@app.route('/brand/<int:brand_id>/guitar/<int:guitar_id>/edit',
           methods=['GET', 'POST'])

def editGuitar(brand_id, guitar_id):
    editedGuitar = session.query(Guitar).filter_by(id=guitar_id).one()
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedGuitar.name = request.form['name']
        if request.form['body_material']:
            editedGuitar.body_material = request.form['body_material']
        if request.form['neck_material']:
            editedGuitar.body_material = request.form['neck_material']
        if request.form['fingerboard_material']:
            editedGuitar.body_material = request.form['fingerboard_material']
        if request.form['frets']:
            editedGuitar.frets = request.form['frets']
        if request.form['scale_length']:
            editedGuitar.scale_length = request.form['scale_length']
        if request.form['pickups']:
            editedGuitar.pickups = request.form['pickups']
        if request.form['bridge']:
            editedGuitar.bridge = request.form['bridge']
        session.add(editedGuitar)
        session.commit()
        return redirect(url_for('showGuitars', brand_id=brand_id))
    else:
        return render_template('editGuitar.html', brand_id=brand_id, guitar_id=guitar_id,
                               guitar=editedGuitar, brands=brands, user=user,
                               username=username, user_id=user_id)

#Delete a brand
@app.route('/brand/<int:brand_id>/delete/', methods=['GET', 'POST'])
def deleteBrand(brand_id):
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    brandToDelete = session.query(Brand).filter_by(id=brand_id).one()
    brandGuitars = session.query(Guitar).filter_by(brand_id=brand_id).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        #Delete the brand
        session.delete(brandToDelete)
        #Delete associated guitars
        for g in brandGuitars:
            session.delete(g)
        session.commit()
        #Determine if brand has image, and if it does, delete it
        brand_id_str = str(brand_id)
        filename = 'logos/' + brand_id_str + '.png'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        #Detemine if brand as associated guitar images, if so, remove guitar images
        guitarImgDirectory = os.path.join(app.config['UPLOAD_FOLDER'], brand_id_str)
        if os.path.isdir(guitarImgDirectory):
            shutil.rmtree(guitarImgDirectory)
        return redirect(
            url_for('showBrands', brand_id=brand_id))
    else:
        return render_template('deleteBrand.html', brand=brandToDelete, brands=brands,
                               user=user, username=username, user_id=user_id)
#Delete a guitar
@app.route('/brand/<int:brand_id>/guitar/<int:guitar_id>/delete',
           methods=['GET', 'POST'])
def deleteGuitar(brand_id, guitar_id):
    brands = session.query(Brand).all()
    user = session.query(User).all()
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        username = login_session['username']
    else:
        user_id = 'none'
        username = 'none'
    guitarToDelete = session.query(Guitar).filter_by(id=guitar_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(guitarToDelete)
        session.commit()
        #Determine if guitar has image and if it does, delete it
        guitar_id_str = str(guitar_id)
        brand_id_str = str(brand_id)
        filename = brand_id_str + '/' + guitar_id_str + '.png'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        return redirect(url_for('showGuitars', brand_id=brand_id))
    else:
        return render_template('deleteGuitar.html', guitar=guitarToDelete, brands=brands,
                               user=user, username=username, user_id=user_id)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
