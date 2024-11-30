from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BaseDATA.db'
db = SQLAlchemy(app)
app.debug = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(200), unique = True, nullable = False)
    password = db.Column(db.Integer, nullable = False)
    date_creation = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    generated_passwords = db.relationship('GeneratedPassword', backref='user', lazy=True)

#Table for Passwords
class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(200), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_creation = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    user = db.relationship('User', backref=db.backref('generated_passwords', lazy=True))

# Create the tables
with app.app_context():
    db.create_all()
    

@app.route('/', methods = ['POST','GET'])
def index():
    return render_template('Index.html')