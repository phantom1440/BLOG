from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from microsoft import p

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = p
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ASDFASqw1221' 

image_path = 'static/images'

app.config['UPLOAD_FOLDER'] = image_path

db = SQLAlchemy(app)
migrate = Migrate(app, db)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'Login'



