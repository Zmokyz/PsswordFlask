from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///BaseDATA.db'
db = SQLAlchemy(app)
app.debug = True

#remember to define the bd here 
# but we're going to do that later bcouse we need to se the tables
# #

@app.route('/', methods = ['POST','GET'])
def index():
    return render_template('Index.html')