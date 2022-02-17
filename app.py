# Importing  necessary packages
from flask import Flask, render_template, request, redirect
'''
-Flask for setting up the application
-render_template for reffering index.html file in static folder in order to interact with it
'''
from flask_sqlalchemy import SQLAlchemy
import git
from datetime import datetime
from os.path import exists

app = Flask(__name__) # Setting up the application
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True	
db = SQLAlchemy(app) # Creating database with binding SQLAlchemy class to our app


class Users(db.Model):
	
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow) # The date that the data created, 'datetime.utcnow' for specifying that moment the data is created
	tasks = db.relationship("Tasks", backref="task", lazy=True)
	
	


# Creating database model with Model instance in SQLAlchemy class
class Tasks(db.Model): 
		
	__tablename__ = "task"
	# Creating columns for database
	id = db.Column(db.Integer, primary_key=True) # Primary key that is gonna be id and do not show up in app in order to handling database with code 
	'''! ! ! ! TO-DO: There is a something wrong with the nullable value the task's name still can be nothing debug it ! ! ! !'''
	content = db.Column(db.String(200), nullable=False) # Creating content key that is gonna be task's name
	date_created = db.Column(db.DateTime, default=datetime.utcnow) # The date that the data created, 'datetime.utcnow' for specifying that moment the data is created
	User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	
		
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data/Users.db' # Setting up the database and route of the file that is gonna store the data
database_exists_U = exists('Data/Users.db') # Creating a bool variable for checking the database exists
if not database_exists_U: # Checking to see if databases is exist
	db.create_all() # If database is not exists create the databases
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data/Tasks.db' # Setting up the database and route of the file that is gonna store the data
database_exists_T = exists('Data/Tasks.db')
if not database_exists_T:
	db.create_all()


# Route for the GitHub webhook
@app.route('/update_server', methods=["POST"])
def webhook():
	if request.method == 'POST':
		repo = git.Repo('./Todo_app_Flask')
		origin = repo.remotes.origin
		origin.pull()
		return 'Updated PythonAnywhere successfully', 200
	else:
		return 'Wrong event type', 400
		
		
@app.route('/', methods=["POST", "GET"])
def index():
	return "debug 1"
	if request.method == 'POST':
		return "debug 2"
		global user_name 						## Creating global user_name variable  
		user_name = request.form['name']		## giving value to user_name variable   ## This two code is gonna be executed when variable calls
		if Users.query.filter_by(name=user_name).first() == None:
			new_user = Users(name=user_name)
			try:
				db.session.add(new_user)
				db.session.commit()
				
			except:
				return "error"
		
		return redirect('/home')
	
		

	return render_template('index.html')
		


# Creating index's route, '/home' is for creating page's url
''' TO-DO: write the comment for methods'''
@app.route('/home', methods = ["POST", "GET"])
def home(): # Function for creating tasks page
	
	
	
	if request.method == 'POST': # If the request that send to this route is POST
		# Create a variable for task's name that is send from html request,
		# "request.form['content']" is for specifying the data that getting from request that we send from html file,
		# html input tag had name='content' attribute for this event
		
		task_content = request.form['content']
		user_id = Users.query.filter_by(name=user_name).first_or_404().id
		# Create a variable that is a todo object that's going to have it's content equal to content of task name that is send from html request
		new_task = Tasks(content=task_content, User_id=user_id) 
		# Pushing Todo object (The data) to our database
		try:
			db.session.add(new_task) # Adding the data to database in session
			db.session.commit() # Commiting the session
			return redirect('/home') # Returning user back to index.html (through route)
		except: # Creating an exception in case of something goes wrong while adding data to database
			return 'There is an error(Adding error)' # If there is something wrong user gonna go to a page saying 'There is an error(Adding error)'
	else: # If the request that send to this route is not POST
		user_id = Users.query.filter_by(name=user_name).first_or_404().id
		tasks = Tasks.query.filter_by(User_id=user_id).all()
		return render_template('home.html', tasks=tasks, username=user_name)

# Creating delete page's route that is not vieweble and just functional, for deleting the data when the user go and clicks the delete link
# The <int:id> is actually the data's id in the database and is needed for function to take as an argument
@app.route('/home/delete/<int:id>')
def delete(id): # Function for deleting data from databse, the id argument is for deleting just the specific data
	task_to_delete = Tasks.query.get_or_404(id) # Creating variable for data to delete in order to defining while using it
	
	try:
		db.session.delete(task_to_delete)  # Deleting the data from database in session
		db.session.commit() # Commiting the session
		return redirect('/home') # Returning user back to index.html
		
	except: # Creating an exception in case of something goes wrong while deleting the data
		return 'There is an error(Deleting error)' #  If there is something wrong user gonna go to a page saying 'There is an error(Deleting error)'

# Creating update page's route for updating the tasks name (or data's content key's string value)
# The <int:id> is actually the data's id in the database and is needed for function to take as an argument
''' TO-DO: write the comment for methods '''
@app.route('/home/update/<int:id>', methods = ["GET", "POST"])
def update(id):# Function for updating the data in database
	print("debug 1")
	task = Tasks.query.get_or_404(id) # Creating a variable for data to update in order to defining while using it
	print("debug 2")
	if request.method == 'POST': # If the request that send to this route is POST
		print("debug 3")
		# Changing task's content to new content
		task.content = request.form['content']
		print("debug 4")
		try:
			db.session.commit() # Commiting the session
			return redirect('/home') # Returning user back to home page
			
		except: # Creating an exception in case of something goes wrong while updating the data
			return 'There is an error(Updating error)' #  If there is something wrong user gonna go to a page saying 'There is an error(Updating error)'
			
	else: # If the request that send to this route is not POST
		print("debug 5")
		return render_template('update.html', task=task, username=user_name) # Then return user to update.html, task=task is  for explaning 'task in html file is the task variable'

if __name__ == "__main__":
	app.run(debug=True)
