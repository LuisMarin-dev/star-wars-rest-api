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
    data = Planet.query.all()
    
    planets_serialize = []
    for item in data:
        planets_serialize.append(item.serialize())
    
    return jsonify(planets_serialize), 200

# this endpoint gets one singular planet's data
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    data = Planet.query.filter_by(id = planets_id).first()

    if data is None:
        return jsonify({"msg":"this planet doesn't exists"})
    
    return jsonify(data.serialize())

# this endpoint gets a list of all the favorites of a singular user (by id)
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    data = Favorite.query.filter_by(user_id = user_id).all()

    favorite_serialize = []
    for item in data:
        favorite_serialize.append(item.serialize())
    
    return jsonify(favorite_serialize), 200

# This endpoint gets a list of all the users
@app.route('/users', methods=['GET'])
def get_users():
    data = User.query.all()
    
    users_serialize = []
    for item in data:
        users_serialize.append(item.serialize())
    
    return jsonify(users_serialize), 200

# This endpoint adds a new planet favorites to the current user
@app.route("/favorite/planet/<int:planet_id>/<int:user_id>", methods=["POST"])
def add_favorite_planet(planet_id, user_id):
    favorite = Favorite.query.filter_by(planet_id = planet_id, user_id = user_id).first()
    
    if favorite is not None:
        return jsonify({"msg":"that planet is already in favorites"})

    new_fav_planet = Favorite(
        planet_id = planet_id,
        user_id = user_id
    )

    db.session.add(new_fav_planet)
    db.session.commit()
    return jsonify(new_fav_planet.serialize()), 200

# This endpoint adds a new character favorites to the current user
@app.route("/favorite/character/<int:character_id>/<int:user_id>", methods=["POST"])
def add_favorite_character(character_id, user_id):
    favorite = Favorite.query.filter_by(character_id = character_id, user_id = user_id).first()
    
    if favorite is not None:
        return jsonify({"msg":"that character is already in favorites"})

    new_fav_character = Favorite(
        character_id = character_id,
        user_id = user_id
    )

    db.session.add(new_fav_character)
    db.session.commit()
    return jsonify(new_fav_character.serialize()), 200

# This endpoint removes a favorite planet
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=["DELETE"])
def remove_favorite_planet(planet_id, user_id):
    favorite = Favorite.query.filter_by(planet_id = planet_id, user_id = user_id).first()

    if favorite is None:
        return jsonify({"msg":"that planet is not in favorites"})

    db.session.delete(favorite)
    db.session.commit()

    return jsonify(favorite.serialize())

# This endpoint removes a favorite character
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=["DELETE"])
def remove_favorite_character(character_id, user_id):
    favorite = Favorite.query.filter_by(character_id = character_id, user_id = user_id).first()

    if favorite is None:
        return jsonify({"msg":"that character is not in favorites"})

    db.session.delete(favorite)
    db.session.commit()

    return jsonify(favorite.serialize())

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=False)