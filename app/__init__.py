import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
from flask_codemirror import CodeMirror
from flask_mail import Mail
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_object(Config)
codemirror = CodeMirror(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login = LoginManager(app)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT', '465')
app.config['MAIL_USE_TLS'] = int(os.environ.get('MAIL_USE_TLS', False))
app.config['MAIL_USE_SSL'] = int(os.environ.get('MAIL_USE_SSL', True))
app.config['MAIL_USERNAME'] = 'noreplycpzen@gmail.com'
app.config['MAIL_PASSWORD'] = 'cpzen1234'
mail = Mail(app)

from app import routes, models
