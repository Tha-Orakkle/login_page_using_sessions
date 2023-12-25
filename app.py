#!/usr/bin/env python3
from flask import (
    Flask,
    g,
    render_template,
    redirect,
    request,
    session,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from os import environ
import uuid


# user = environ.get('PAGE_USER')
# pwd = environ.get('PAGE_PWD')
# host = environ.get('PAGE_HOST')
# database = environ.get('PAGE_DB')


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{pwd}@{host}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_page_test.db'
app.secret_key = 'somethingonlyIshouldknow'
db = SQLAlchemy(app)



class User(db.Model):
    """Represents a user"""
    __tablename__ = 'users'
    id = db.Column(db.String(128), unique=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    
    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
    
    def __repr__(self):
        """internal representation of the User Object"""
        return f"<User> [{self.id}] {self.username}"
    

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        usr = db.session.query(User).filter(User.id == session['user_id']).first()
        g.user = usr


@app.route('/login', methods=['GET', 'POST'])
def login():
    # session.pop('user_id', None)
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        passwd = request.form['password']
        usr = db.session.query(User).filter(User.username == username).first()
        # usr = User.query.filter_by(username=username).first()
        if usr and usr.password == passwd:
            session['user_id'] = usr.id
            return redirect(url_for('profile'))
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True)