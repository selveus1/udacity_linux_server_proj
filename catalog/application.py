from flask import Flask
from flask import render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)
app.secret_key = "super secret key"

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import populatedb
import requests


CLIENT_ID = json.loads(open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


# connect to database and establish a database session
#engine = create_engine('postgresql+psycopg2://catalog:udacity@localhost/catalog')
#engine = create_engine('postgresql://catalog:udacity@http://ec2-18-221-132-70.us-east-2.compute.amazonaws.com/catalog')
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#######################
# user helper functions
#######################

def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
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


#######################
# application functions
#######################
# login for users with Google Accounts 
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + 
		string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


# connecting page for authorized google users
@app.route('/gconnect', methods=['POST'])
def gconnect():
	# check state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# get authorization code
	request.get_data()
	code = request.data.decode('utf-8')

	try:
		# upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalog/client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# check that the access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	# submit token, parse response
	h = httplib2.Http()

	#result = json.loads(h.request(url, 'GET')[1])
	response = h.request(url, 'GET')[1]
	str_response = response.decode('utf-8')
	result = json.loads(str_response)

	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# verify that access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# verify that the access token is valid for this app
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# store the access token in the session for later use
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# check if user exists, make one if not
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	# render a welcome page
	flash("You are now logged in as %s" % login_session['username'])
	print "done!"
	return render_template('welcome.html', user=login_session['username'], picture=login_session['picture'])


# logout link for authorized users
@app.route('/gdisconnect')
def gdisconnect():
	access_token = login_session.get('access_token')
	print 'In gdisconnect access token is %s', access_token

	print login_session['username']
	username = login_session['username']

	if access_token is None:
		print 'Access Token is None'
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		# delete all of logged in user info
		del login_session['access_token'] 
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		# render a logout page
		response = make_response(render_template('logout.html', response=username), 401)
		response.headers['Content-Type'] = 'text/html'
		return response

	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


# show all the categories
@app.route('/')
@app.route('/catalog/')
def showCategories():

	# grab the catagories and most recently added items
	categories = session.query(Category).order_by(asc(Category.name))
	items = session.query(Item).order_by(asc(Item.date_added)).limit(8)

	# not legged in so grab the public page
	if 'username' not in login_session:
		user = ""
		return render_template('publiccatalog.html', categories=categories, items=items)
	else:	
		user = login_session['username']
		return render_template('catalog.html', user=user, categories=categories, items=items)


# show all items in a category
@app.route('/catalog/<int:category_id>/items')
def showCategoryItems(category_id):
	# grab the specfic catagory and the items belonging to that category
	category = session.query(Category).filter_by(id=category_id).one()
	items = session.query(Item).filter_by(category_id=category.id).order_by(asc(Item.name))

	# not legged in so grab the public page
	if 'username' not in login_session:
		return render_template('publicitems.html', category=category, items=items)
	else:
		user = login_session['username']
		return render_template('items.html', user=user, category=category, items=items)
		

# show item
@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
	category = session.query(Category).filter_by(id=category_id).one()
	item = session.query(Item).filter_by(id=item_id).one()

	# not legged in so grab the public page
	if 'username' not in login_session:
		return render_template('showpublicitem.html',category=category, item=item)
	else:
		user = login_session['username']
		return render_template('showitem.html', user=user, category=category, item=item)


# create a new category item
@app.route('/catalog/item/new', methods=['GET', 'POST'])
def newItem():

	# not a valid user so redirect to catalog page
	if 'username' not in login_session:
		print 'not here'
		flash('You have to log in to create items!')
		return redirect('/catalog')

	# posting so create item
	if request.method == 'POST':
		# create item and assign it to its category
		category = session.query(Category).filter_by(name=request.form['category']).one()

		newItem = Item(name=request.form['name'], description=request.form['description'], category_id=category.id, user_id=login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash('New %s Item Successfully Created' % (newItem.name))
		return redirect(url_for('showCategoryItems', category_id=category.id))
	else: #render the form page
		categories = session.query(Category).order_by(asc(Category.name))
		return render_template('newitem.html', user=login_session['username'], categories=categories)	


# edit item
@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):

	# not a valid user so redirect to catalog page
	if 'username' not in login_session:
		print 'not here'
		flash('You have to log in to edit items!')
		return redirect('/catalog')

	item = session.query(Item).filter_by(id=item_id).one()
	category = session.query(Category).filter_by(id=item.category_id).one()

	# check if user can edit
	if item.user_id != login_session['user_id']:
		flash('You are not authorized to edit this item. Please create your own item in order to edit.')
		return redirect(url_for('showCategoryItems', category_id=category.id))

	# logged in user and valid user
	if request.method == 'POST':
		# grab what has changed
		if request.form['name']:
			item.name = request.form['name']
		if request.form['description']:
			item.description = request.form['description']
		if request.form['category']:
			category = session.query(Category).filter_by(name=request.form['category']).one()
			if category:
				item.category_id = category.id

		session.add(item)
		session.commit()
		flash('%s Item Successfully Edited!' % (item.name))
		return redirect(url_for('showCategoryItems', category_id=category.id))
	else:
		categories = session.query(Category).order_by(asc(Category.name))
		return render_template('edititem.html', user=login_session['username'], item=item, categories=categories)



# delete item
@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
	# not a valid user so redirect to catalog page
	if 'username' not in login_session:
		print 'not here'
		flash('You have to log in to delete items!')
		return redirect('/catalog')

	item = session.query(Item).filter_by(id=item_id).one()
	category = session.query(Category).filter_by(id=item.category_id).one()

	# check if user can delete
	if item.user_id != login_session['user_id']:
		flash('You are not authorized to delete this item. You can only delete items you have created.')
		return redirect(url_for('showCategoryItems', category_id=category.id))

	# logged in user and valid user
	if request.method == 'POST':
		item_name = item.name
		category_name = item.category.name
		session.delete(item)
		session.commit()
		flash('%s Item Successfully Deleted!' % item_name)
		return redirect(url_for('showCategoryItems', category_id=category.id))
	else:
		return render_template('deleteitem.html', user=login_session['username'], item=item)


######################
# JSON APIs functions
######################
@app.route('/catalog/JSON')
def showJSONCatalog():
	categories = session.query(Category).all()

	catalog = []
	for c in categories:

		items = session.query(Item).filter_by(
		category_id=c.id).all()

		c_dict = c.serialize
		c_dict.update(Items=[i.serialize for i in items])
		catalog.append(c_dict)
	
	return jsonify(categories=catalog)	


@app.route('/catalog/categories/JSON')
def showJSONCategories():
	categories = session.query(Category).all()
	return jsonify(categories=[c.serialize for c in categories])	


@app.route('/catalog/items/JSON')
def showJSONItems():
	items = session.query(Item).all()
	return jsonify(Items=[i.serialize for i in items])


if __name__ == '__main__':
	#app.secret_key = 'super_secret_key'
	app.debug = True
	#app.run(host = '0.0.0.0', port = 8000)
