from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'some_secret'
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280))
    last_name = db.Column(db.String(120))
    phone_numbe = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()
