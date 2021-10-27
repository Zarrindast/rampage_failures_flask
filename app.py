# #!/usr/bin/env python  <---- what is this for YOU?
# encoding: utf-8

from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import requests
# we get Model baseclass for free from flask-sqlalchemy
# check underscore vs dash
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, redirect

#from admin.admin import admin_app

app = Flask(__name__)
#app.register_blueprint(admin_app)


app.config["ENV"] = 'development'
app.config["SECRET_KEY"]=b'yeahyeahtotallysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///failed_shooting_attempts_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#####

db = SQLAlchemy(app)

class AttemptClass(db.Model): #https://flask-user.readthedocs.io/en/latest/data_models.html
    __tablename__ = "Failed School Shooting Attempts"
    # notice that this class doesn't even def __init__ and have instance attributes possible
    # these are all class attributes because there is only ever this one instance
    # is this... okay?
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    person = db.Column(db.String(255),nullable=True)
    description = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<Attempt:{}--{}--{}--{}--{}>".format(self.id, self.date, self.location, self.person, self.description) 

class UserClass(db.Model): #https://flask-user.readthedocs.io/en/latest/data_models.html
    __tablename__ = "Users Registered"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<User {self.id}: username={self.username}, password={self.password}"



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/d3')
def show():
    return render_template("d3smiley.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        new_un = flask.request.values.get["username"]
        new_pw = flask.request.values.get["password"]
        new_user = UserClass(username=new_un, password=new_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template("register.html")


@app.route('/page1')
def page1():
     return render_template('page1.html')

@app.route('/page1/<page1_id>')
def page1_post1(page1_id):
    return "This is page1 post number " + str(page1_id)

# # change this to return your data
# @app.route('/api', methods=['GET'])
# def get_data():
#     table = DBTable.query.all()
#     d = {row.column_1:row.column_2 for row in table}
#     return jsonify(d)

@app.route('/api', methods=['GET'])
def get_records():
    if request.method == 'GET':
        table = AttemptClass.query.all()
        retrieved_data = {f"{row.id}": [f"{row.date}",f"{row.location}",f"{row.person}",f"{row.description}"] for row in table}
        return jsonify(retrieved_data)
        # note: do not use json.dumps(blah) 
        # that is a string and the browser will think it's html while YOU may think it's /want json
        # jsonify is a function that is part of Flask

@app.route('/api', methods=['POST'])
# find some way to get message to users before or during the post since the info is complex
def instruct_user():
    return "format your entry like such and such." # or could do a var that's HTML in triple quotes
def create_record():
        table = AttemptClass.query.all()
        #people = AttemptClass.person.query.all() # not sure if valid
        #added = {}
        new_attack_date = request.args["date"]
        new_attack_location = request.args["location"]
        new_attack_person = request.args["person"]
        new_attack_description = request.args["description"]
        # if not new_attack_person in AttemptClass.person.query.all()
        new_attack = AttemptClass(date=new_attack_date,location=new_attack_location,person=new_attack_person,description=new_attack_description)
        db.session.add(new_attack)
        db.session.commit()

        return jsonify({"added": new_attack, "current": table})
        # returning a minidict that shows you the new entry as a value under the label "added"
        # and the total so far post-POST under the label "current"

        # ideally, search by person, year, or state (will have to separate out city and state)

        
# # change this to allow the deletion of data
# @app.route('/api', methods=['DELETE'])
# def delete_data():
#     for k,v in request.args.items():
#         pass
#     return jsonify({})

#

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = flask.request.values.get['nm']
#       return "hi, {user}!"
#    else:
#       user = request.args.get('nm')
#       return "#redirect(url_for('login',name = user))"

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#     user = request.values.get['nm']
#     return "hi, {user}!"


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
