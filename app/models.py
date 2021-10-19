from sqlalchemy.orm import backref
from app import app, db, login
from datetime import datetime
from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import app
# from config import Config
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    save_codes = db.relationship('SaveCode', backref='coder', lazy='dynamic')
    temp_codes = db.relationship('tempCode', backref='coder', lazy='dynamic')
    algorithm_table = db.relationship('Algorithm', backref='coder', lazy='dynamic')

 
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'"

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.username)
        # return '<User {}>'.format(self.username)
          


class SaveCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_code = db.Column(db.String(10000))
    code_name = db.Column(db.String(1000))
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{}-----{}'.format(self.code_name, self.source_code)
    
    # def __repr__(self):
    #     return ''.format(self.code_name)

class tempCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_code = db.Column(db.String(10000))
    # saved_name = db.Column(db.String(100))
    code_name = db.Column(db.String(1000))
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{}-----{}'.format(self.code_name, self.temp_code)
    
class Algorithm(db.Model):
    algorithm_id = db.Column(db.Integer, primary_key=True)
    algo_type = db.Column(db.String(1000))
    algo_name = db.Column(db.String(1000))
    algo_resources = db.Column(db.String(10000))
    algo_problems = db.Column(db.String(10000))
    algo_proficiency = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{}-----{}-----{}-----{}-----{}-----{}'.format(self.algorithm_id, self.algo_type, self.algo_name, self.algo_resources, self.algo_problems, self.algo_proficiency)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))