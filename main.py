from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os

from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab6.db'
app.config['SEVER_NAME'] = os.environ.get("SERVER_NAME", default="127.0.0.1")
db = SQLAlchemy(app)

# use localhost for your local machine
# host = "localhost" 
host = app.config['SEVER_NAME']

# enable CORS on all the routes that start with /api
CORS(app, resources={r"/api/*": {"origins": "*"}})

##********************************* Models *************************************

# Standard model setup. refer to sqlachemy docs
class Person(db.Model):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(50), unique=True)
    date_created = Column(DateTime(), server_default=func.now())
    country = Column(String(3), default='TnT')
    
    #constructor for class good idea to make one
    def __init__(self, name = None, country = None):
        self.name = name
        self.country = country
        

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'country': self.country
        }

#db.create_all()

#********************************Data Functions ********************************
# These functions perform operations on the database and are used by the routes
# They all use python try catch to prevent the server from crashing on error
# Lab 6 has similiar functionality in routes
# All functions return a dictionary which is jsonified when they are called in the routes
# It is not necessary to separate these functions from the routes. However, they were separated so
# that they can be reused in different routes

def createPerson(new_person):
    try:
        p = Person(new_person['name'], new_person["country"])#create person object using contructor
        db.session.add(p)
        db.session.commit()# save object
    except error:
        return {"message":"Error "+error, "code":500}
    finally:
        return {"message":p.toDict(), "code":201}
        
def updatePerson(new_person, id):
    try:
        p = Person.query.get(id)
        p.name = new_person['name']# over write object property
        p.country = new_person["country"]# save object
        db.session.commit()#save object
    except error:
        return {"message":"Error "+error, "code":500}
    finally:
        return {"message":p.toDict(), "code":202}

def deletePerson(id):
    try:
        p = Person.query.get(id)
        db.session.delete(p)#delete object from database
        db.session.commit()#save changes
    except error:
        return {"message":"Database error"+error, "code":500}
    finally:
        return {"message": "Record Deleted", "code": 204}

# *********************************APP1 ROUTES**********************************
# View Routes & Data Routes 
# The post routes are only compatible with form data not json
# Templating routes return render_template() done in Lab 7

# Allows static files to be requested eg js,css, images
# @app.route('/static/<path>')
# def static(path):
#     return send_from_directory('templates', path)

# Serves specific files through flask
@app.route('/app1.png')
def app1_png():
    return send_from_directory('templates', 'app1.png')
    
@app.route('/app2.png')
def app2_png():
    return send_from_directory('templates', 'app2.png')

@app.route('/config.js')
def configjs():
    return send_from_directory('templates', 'config.js')

# get all persons and pass it to a template to render
@app.route('/app1')
def app1():
    records = Person.query.all()
    records = list(map(lambda object: object.toDict(), records))
    response = jsonify(records)
    return render_template("app1.html", person=None, records=records, host=host)

# full js version of app no templating done on server
@app.route('/app2')
def app2():
    return send_from_directory('templates', "app2.html")

@app.route("/")
def index():
    return render_template("index.html")

#passes which record to be updated into the template
@app.route("/update/<id>")
def update(id):
    p = Person.query.get(id)
    records = Person.query.all()
    records = list(map(lambda object: object.toDict(), records))
    response = jsonify(records)
    return render_template("app1.html", person=p, host=host, records=records)

@app.route('/persons', methods=['GET'])
def show_all_persons():
    records = Person.query.all()
    records = list(map(lambda object: object.toDict(), records))#must convert objects to dictionaries
    response = jsonify(records)#jsonify all responses which aren't templates
    response.status_code = 200
    return response

@app.route('/persons/<id>', methods=['GET'])
def show_person(id):
    return jsonify(Person.query.get(id).toDict())

@app.route('/persons', methods=['POST'])
def save_person():
    if request.content_type  == 'application/x-www-form-urlencoded': #would not work if json data is sent
        result = createPerson(request.form)
        if result['code'] == 201:#201 Created, set by createPerson on successful create
             return app1()# redirect to home
        else:
            return render_template('error.html', result=result)
    render_template('error.html', result={"message":"Invliad data format", "code":500})

@app.route('/persons/update', methods=['POST'])
def udpate_person():
    id = request.form['id']
    result = updatePerson(request.form, id)
    if result['code'] == 202:#202 Accepted, set by updatePerson on successful update
        return app1()# redirect to home
    else:
        return render_template('error.html', result=result)

@app.route('/persons/delete/<id>', methods=['GET'])
def remove_person(id):
    result = deletePerson(id)
    if result['code'] == 204:#204 No content, set by deletePerson if deletion was successful
        return app1()# redirect to home
    else:
        return render_template('error.html', result=result)

    
# ******************************* APP2 Routes **********************************
## Data only Routes, no rendering done
## The data can be received in the routes as either json or form data


@app.route('/api/persons/<id>', methods=['GET'])
def api_get_person(id):
    return jsonify(Person.query.get(id).toDict())

@app.route('/api/persons', methods=['GET'])
def api_get_persons():
    records = Person.query.all()
    records = list(map(lambda object: object.toDict(), records))
    response = jsonify(records)
    response.status_code = 200
    return response


@app.route('/api/persons', methods=['POST'])
def api_create_person():
    data = None
    if request.content_type  == 'application/x-www-form-urlencoded':
        data = request.form
    elif request.content_type == 'application/json':
        data = request.json
    return jsonify(createPerson(data))# call createPerson on data an jsonify its response

@app.route('/api/persons/<id>', methods=['PUT'])
def api_update_person(id):
    data = None
    if request.content_type  == 'application/x-www-form-urlencoded':
        data = request.form
    elif request.content_type == 'application/json':
        data = request.json
    return jsonify(updatePerson(data, id))

@app.route('/api/persons/<id>', methods=['DELETE'])
def api_delete_person(id):
    return jsonify(deletePerson(id))


# if __name__ == "__main__":
#     print("Running From the Command line")
#     app.run(host='0.0.0.0', debug=True, use_reloader=True)