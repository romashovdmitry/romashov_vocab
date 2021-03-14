from flask_login import UserMixin
from config_file import db

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    user_password = db.Column(db.String(300))
     
class whole_vocab(db.Model):
    id_in_whole = db.Column(db.Integer, primary_key=True)
    word_in_whole = db.Column(db.String(200))
    definition_of_word = db.Column(db.String(2000))
    user_id = db.Column(db.Integer)