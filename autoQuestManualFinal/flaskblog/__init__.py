from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector import errorcode

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from flaskblog import routes