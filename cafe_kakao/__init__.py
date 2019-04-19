# -*- coding: utf-8 -*-

import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

config = configparser.ConfigParser()
config.read('./config.ini')
REST_API_KEY = config['SECRET']['REST_API_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['REST_API_KEY'] = config['SECRET']['REST_API_KEY']
app.config['SERVER_ENV'] = config['DEFAULT']['SERVER_ENV']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from cafe_kakao import routes  # 위치 바꾸지 마라
