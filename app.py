from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json


from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab6.db'
db = SQLAlchemy(app)

host = "https://extra-snickdx.c9users.io:8080"

# enable CORS on all the routes that start with /api
CORS(app, resources={r"/api/*": {"origins": "*"}})

##********************************* Models *************************************
class Person(db.Model):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(50), unique=True)
    date_created = Column(DateTime(), server_default=func.now())
    country = Column(String(3), default='TnT')

    def __init__(self, name, country = None):
        self.name = name
        if country:
            self.country = country
        

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created,
            'country': self.country
        }

#db.create_all()

##*********************************** Functions ********************************

def createPerson(new_person):
    if 'name' in new_person:
        p = Person(new_person['name'])
    else:
        return {"message":"Invalid fields given", "code":400}
    if 'country' in new_person:
        p.country = new_person["country"]
    try:
        db.session.add(p)
        db.session.commit()
    except error:
        return {"message":"Error "+error, "code":500}
    finally:
        return {"message":p.toDict(), "code":201}
        
def updatePerson(new_person, id):
    p = Person.query.get(id)
    try:
        if 'name' in new_person:
            p.name = new_person['name']
        else:
            return {"message":"Invalid fields given", "code":400}
        if 'country' in new_person:
            p.country = new_person["country"]
        db.session.commit()
    except error:
        return {"message":"Error "+error, "code":500}
    finally:
        return {"message":p.toDict(), "code":202}

def deletePerson(id):
    try:
        p = Person.query.get(id)
        db.session.delete(p)
        db.session.commit()
    except error:
        return {"message":"Database error"+error, "code":500}
    finally:
        return {"message": "Record Deleted", "code": 204}

# *********************************APP1 ROUTES**********************************
# View Routes & Data Routes 


@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('templates/js', path)
    
@app.route('/app1')
def app1():
    records = Person.query.all()
    records = list(map(lambda object: object.toDict(), records))
    response = jsonify(records)
    return render_template("app1.html", person=None, records=records, host=host)
    
@app.route('/app2')
def app2():
    return send_from_directory('templates', "app2.html")

@app.route("/")
def index():
    return render_template("index.html")
    
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
    records = list(map(lambda object: object.toDict(), records))
    response = jsonify(records)
    response.status_code = 200
    return response

@app.route('/persons/<id>', methods=['GET'])
def show_person(id):
    return jsonify(Person.query.get(id).toDict())

@app.route('/persons', methods=['POST'])
def save_person():
    if request.content_type  == 'application/x-www-form-urlencoded':
        result = createPerson(request.form)
        if result['code'] == 201:
             return index()
        else:
            return render_template('error.html', result=result)
    render_template('error.html', result={"message":"Invliad data format", "code":500})

@app.route('/persons/update/<id>', methods=['POST'])
def udpate_person(id):
    result = updatePerson(request.form, id)
    if result['code'] == 202:
        return index()
    else:
        return render_template('error.html', result=result)

@app.route('/persons/delete/<id>', methods=['GET'])
def remove_person(id):
    result = deletePerson(id)
    if result['code'] == 204:
        return index()
    else:
        return render_template('error.html', result=result)

    
# ******************************* APP2 Routes **********************************
## Data only Routes, no rendering done


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
    return jsonify(createPerson(data))

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