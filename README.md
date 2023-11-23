# to-do-list

## Todo Flask App

This project implements a simple task management web application using Flask, allowing users to manage their tasks and profiles efficiently.

Features

User Authentication: Enables users to log in and manage their tasks securely.
Task Management: Users can add, delete, mark tasks as done, and prioritize them as needed.
User Profiles: Provides the ability to set up and edit user profiles with usernames and full names.
Setup Instructions

Clone the Repository
```
Copy code
git clone https://github.com/your_username/todo-flask-app.git
cd todo-flask-app
Install Dependencies
bash
Copy code
pip install -r requirements.txt
Database Setup
Ensure SQLite is installed.
Initialize the database by running:
bash
Copy code
python app.py
Run the Application
bash
Copy code
python app.py
Access the App
Visit http://localhost:5000/ in your web browser to use the application.
Usage

Upon accessing the application:

Users can either log in with existing credentials or create a new account.
Tasks can be added by providing a title, description, and optional priority setting.
Task management includes marking tasks as done or deleting them.
Users can modify their profiles by clicking on "Edit Profile".
Technologies Used

This project utilizes the following technologies:

Python
Flask
SQLAlchemy (SQLite)
HTML/CSS
Semantic UI
Code Description

The main functionalities of the Flask app include:

User Authentication (Login/Logout):
/login: Handles user authentication and session management.
/logout: Logs the user out and redirects to the login page.
Task Management:
/add: Adds tasks to the user's task list.
/done/<int:todo_id>: Marks tasks as done or undone.
/delete/<int:todo_id>: Deletes tasks from the list.
User Profile:
/profile: Allows users to view and update their profile information.
/save_changes: Saves changes made to the user profile.
/go_back: Redirects the user back to the home page.
Contributors

Your Name - Role/Contributions
License

This project is licensed under the MIT License.

