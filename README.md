# Flask To-Do App with User-Based Task Management

A simple to-do app built with Flask and Flask-SQLAlchemy. Each user logs in with a username and sees only their own tasks, stored in a relational database.

🌐 **Live Demo:** [limonyerinelimon.pythonanywhere.com](http://limonyerinelimon.pythonanywhere.com/)

## Features

- User-based task management without password authentication
- Relational database with **Users** and **Tasks** tables
- Each task is linked to a user via a foreign key
- Automatic user creation on login if username does not exist
- Persistent storage using **Flask-SQLAlchemy**

## How It Works

1. When a user enters a username:
   - The app checks the `Users` table.
   - If the user does not exist, a new user is created.
2. The app then queries the `Tasks` table for any tasks tied to that user.
3. The user can view, add, and delete their own tasks.
