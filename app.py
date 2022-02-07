# Importing  necessary packages
from flask import Flask, render_template, request, redirect
'''
-Flask for setting up the application
-render_template for reffering index.html file in static folder in order to interact with it
'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os.path import exists
import git


app = Flask(__name__) # Setting up the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Setting up the database and route of the file that is gonna store the data, file's name is gonna be test.db
db = SQLAlchemy(app) # Creating database with binding SQLAlchemy class to our app

# Route for the GitHub webhook
@app.route('/update_server', methods=['POST'])
def webhook():
	if request.method == 'POST':
		repo = git.Repo('./Todo_app_Flask')
		origin = repo.remotes.origin
		origin.pull()
		return 'Updated PythonAnywhere successfully', 200
	else:
		return 'Wrong event type', 400

# Creating database model with Model instance in SQLAlchemy class
class Todo(db.Model): 

	# Creating columns for database
	id = db.Column(db.Integer, primary_key=True) # Primary key that is gonna be id and do not show up in app in order to handling database with code 
	'''! ! ! ! TO-DO: There is a something wrong with the nullable value the task's name still can be nothing debug it ! ! ! !'''
	content = db.Column(db.String(200), nullable=False) # Creating content key that is gonna be task's name
	date_created = db.Column(db.DateTime, default=datetime.utcnow) # The date that the data created, 'datetime.utcnow' for specifying that moment the data is created
	
	def __repr__(self): # ???
		return '<Task %r>' % self.id # ???

# Creating index's route, '/' is for creating page's url
''' TO-DO: write the comment for methods'''
@app.route('/', methods = ['POST', 'GET'])
def index(): # Function for creating home page

	database_exists = exists('test.db') # Creating a bool variable for checking database exist
	if not database_exists: # Checking to see if database is exist
		db.create_all() # If database is not exists create the database
	
	
	if request.method == 'POST': # If the request that send to this route is POST
		# Create a variable for task's name that is send from html request,
		# "request.form['content']" is for specifying the data that getting from request that we send from html file,
		# html input tag had name='content' attribute for this event
		task_content = request.form['content']
		# Create a variable that is a todo object that's going to have it's content equal to content of task name that is send from html request
		new_task = Todo(content=task_content) 
		
		# Pushing Todo object (The data) to our database
		try:
			db.session.add(new_task) # Adding the data to database in session
			db.session.commit() # Commiting the session
			return redirect('/') # Returning user back to index.html
		except: # Creating an exception in case of something goes wrong while adding data to database
			return 'There is an error(Adding error)' # If there is something wrong user gonna go to a page saying 'There is an error(Adding error)'
	else: # If the request that send to this route is not POST
	
		# Creating a tasks variable for html to show tasks in webpage
		'''! ! ! ! TO-DO: idk what query means for now, look at it ! ! ! !'''
		# .order_by(Todo.date_created) for ordering the data with date
		# .all() is for getting all of the data
		tasks = Todo.query.order_by(Todo.date_created).all() 
		
		return render_template('index.html', tasks=tasks) # Returning index.html file in the static file to user, task=task is  for explaning ' tasks in html file is the tasks variable'
		
# Creating delete page's route that is not vieweble and just functional, for deleting the data when the user go and clicks the delete link
# The <int:id> is actually the data's id in the database and is needed for function to take as an argument
@app.route('/delete/<int:id>')
def delete(id): # Function for deleting data from databse, the id argument is for deleting just the specific data
	task_to_delete = Todo.query.get_or_404(id) # Creating variable for data to delete in order to defining while using it
	
	try:
		db.session.delete(task_to_delete)  # Deleting the data from database in session
		db.session.commit() # Commiting the session
		return redirect('/') # Returning user back to index.html
		
	except: # Creating an exception in case of something goes wrong while deleting the data
		return 'There is an error(Deleting error)' #  If there is something wrong user gonna go to a page saying 'There is an error(Deleting error)'

# Creating update page's route for updating the tasks name (or data's content key's string value)
# The <int:id> is actually the data's id in the database and is needed for function to take as an argument
''' TO-DO: write the comment for methods'''
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):# Function for updating the data in database
	task = Todo.query.get_or_404(id) # Creating a variable for data to update in order to defining while using it
	
	if request.method == 'POST': # If the request that send to this route is POST
		# Changing task's content to new content
		task.content = request.form['content']
		
		try:
			db.session.commit() # Commiting the session
			return redirect('/') # Returning user back to home page
			
		except: # Creating an exception in case of something goes wrong while updating the data
			return 'There is an error(Updating error)' #  If there is something wrong user gonna go to a page saying 'There is an error(Updating error)'
			
	else: # If the request that send to this route is not POST
		return render_template('update.html', task=task) # Then return user to update.html, task=task is  for explaning 'task in html file is the task variable'
	
if __name__ == "__main__":
	app.run(debug=True)
