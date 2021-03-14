# different Flask packages 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_login import LoginManager, UserMixin
from flask_script import Manager
from flask_sslify import SSLify
from flask_migrate import Migrate, MigrateCommand
# for requests to DB 
import psycopg2
# logging packages 
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

sslify = SSLify(app)
app.config['SECRET_KEY'] = '<secret key>'
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = '<dialect+driver://username:password@host:port/database://>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

import routes

conn = psycopg2.connect( host=host, user=user, password=password, dbname=dbname)
 
def db_update(comd):
    '''For inserting, updating and deleting data from DB'''
    cursor = conn.cursor()
    cursor.execute(comd)
    conn.commit()

def db_select(comd):
    '''For getting data from DB'''
    cursor = conn.cursor()
    cursor.execute(comd)
    results = cursor.fetchall()
    return(results)

logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  : %(levelname)s : %(message)s')
logger = logging.getLogger('telegram_logger')
handler = RotatingFileHandler(filename="romashov_bot.log", maxBytes=9000, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

def ex_catcher(user_id, foo_name, ex):
    '''Foo for writing erors to Log file'''
    logger.error("У пользователя №{} в функции с названием <{}> возникла ошибка следующая <{}> ".
                format(str(user_id), str(foo_name), str(ex)))