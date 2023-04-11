#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Welcome to Camping Fun!</h1>'

@app.route('/campers', methods=['GET', 'POST'])
def campers():
    if request.method == 'GET':
        campers_list = [ camper.to_dict(rules=('-signups',)) for camper in Camper.query.all() ]
        return make_response(campers_list, 200)
    elif request.method == 'POST':
        data = request.get_json()
        new_camper = Camper(
            name = data['name'],
            age = data['age']
        )
        db.session.add(new_camper)
        db.session.commit()

        return make_response(new_camper.to_dict(rules=('-signups',)), 201)

@app.route('/campers/<int:id>')
def camper_by_id(id):
    found_camper = Camper.query.filter(Camper.id == id).first()
    if found_camper:
        return found_camper.to_dict(rules=('-signups', 'activities'))
    return make_response({'error': '404: Camper not found'}, 404)

@app.route('/activities', methods=['GET'])
def activities():
    activities = [ activity.to_dict(rules=('-signups',)) for activity in Activity.query.all()]
    return make_response(activities, 200)

@app.route('/activities/<int:id>', methods=['DELETE'])
def activity_by_id(id):
    found_activity = Activity.query.filter(Activity.id == id).first()
    if not found_activity:
        return make_response( { 'error': '404: Activity not found' }, 404)
    elif request.method == 'DELETE':
        db.session.delete(found_activity)
        db.session.commit()
        return {}, 204
    
@app.route('/signups', methods=['POST'])
def signups():
    data = request.get_json()
    try:
        new_signup = Signup(
            time = data['time'],
            camper_id = data['camper_id'],
            activity_id = data['activity_id']
        )
        db.session.ad(new_signup)
        db.session.commit()
        return make_response(new_signup.to_dict(), 201)
    except ValueError:
        return { "error": "400: Validation error" }, 400
        



if __name__ == '__main__':
    app.run(port=5555, debug=True)
