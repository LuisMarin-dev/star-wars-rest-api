"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this endpoint gets a list of all the characters
@app.route('/people', methods=['GET'])
def get_people():
    data = Character.query.all()
    
    people_serialize = []
    for item in data:
        people_serialize.append(item.serialize())
    
    return jsonify(people_serialize), 200

# this endpoint gets one singular character's data
@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    data = Character.query.filter_by(id = people_id).first()

    if data is None:
        return jsonify({"msg":"this character doesn't exists"})
    
    return jsonify(data.serialize())

# this endpoint gets a list of all the planets
@app.route('/planets', methods=['GET'])
def get_planets():
    data = Character.query.all()
    
    planets_serialize = []
    for item in data:
        planets_serialize.append(item.serialize())
    
    return jsonify(planets_serialize), 200

# this endpoint gets one singular planet's data
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    data = Planets.query.filter_by(id = planets_id).first()

    if data is None:
        return jsonify({"msg":"this planet doesn't exists"})
    
    return jsonify(data.serialize())

# this endpoint adds items to the "favorites" model
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    data = Favorite.query.filter_by(user_id = user_id).all()

    favorite_serialize = []
    for item in data:
        favorite_serialize.append(item.serialize())
    
    return jsonify(favorite_serialize), 200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=False)