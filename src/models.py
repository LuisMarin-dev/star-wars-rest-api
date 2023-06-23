import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
# ################ from SW Data Modeling ##################### 
class User(db.Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Character(db.Base):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    mass = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10))

class Planet(db.Base):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    climate = db.Column(db.String(10), nullable=False)
    gravity = db.Column(db.String(10), nullable=False)
    terrain = db.Column(db.String(20), nullable=False)

class Starship(db.Base):
    __tablename__ = "starship"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    model = db.Column(db.String(10), nullable=False)
    manufacturer = db.Column(db.String(10), nullable=False)
    hyperdrive_rating = db.Column(db.String(20), nullable=False)

class Favorite(db.Base):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, ForeignKey("character.id"))
    planet_id = db.Column(db.Integer, ForeignKey("planet.id"))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    starship_id = db.Column(db.Integer, ForeignKey("starship.id"))

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')