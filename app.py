from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    full_name = db.Column(db.String(100))

    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    done = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prio = db.Column(db.Boolean, default=False)

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for("login"))
    
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    if user:
        full_name = user.full_name
        todo_list = user.todos[::-1]
    else:
        full_name = None
        todo_list = []

    todo_list = user.todos[::-1] if user else []

    return render_template("base.html", todo_list=todo_list, username=username, full_name=full_name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()

        if not user:
            new_user = User(username=username, full_name=None)
            db.session.add(new_user)
            db.session.commit()

        session['username'] = username

        if user and user.full_name:
            session['full_name'] = user.full_name 

        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    prio = 'prio' in request.form
    username = session.get('username')

    user = User.query.filter_by(username=username).first()

    todo = Todo(title=title, description=description, done=False, prio=prio, user_id=user.id)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/done/<int:todo_id>")
def done(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/save_changes', methods=['POST'])
def save_changes():
    return redirect(url_for('profile'))

@app.route('/go_back', methods=['POST'])
def go_back():
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    full_name = user.full_name

    message = None

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_fullname = request.form.get('full_name')

        if user:
            if new_username and new_username != user.username:
                existing_user = User.query.filter_by(username=new_username).first()
                if existing_user:
                    message = "Username already exists. Please choose a different one."
                else:
                    user.username = new_username
                    session['username'] = new_username 

            if new_fullname:
                user.full_name = new_fullname
                session['full_name'] = new_fullname

            db.session.commit()

            return redirect(url_for('profile'))

    return render_template("profile.html", username=username, full_name=full_name, message=message)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
