from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    """individual users"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        )
    user_name = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False, unique=False)


class My_Recipe(db.Model):
    """individual recipes"""

    __tablename__ = 'my_recipes'

    recipe_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True,
                          )
    recipe_name = db.Column(db.String(100), nullable=False, unique=False,)
    ingredients = db.Column(db.String(5000), nullable=False, unique=False,)
    directions = db.Column(db.String(5000), nullable=False, unique=False,)
    ratings = db.Column(db.Integer, nullable=True, unique=False,)
    prep_time = db.Column(db.String(25), nullable=False, unique=False,)
    cook_time = db.Column(db.String(25), nullable=False, unique=False,)
    cuisine = db.Column(db.String(25), nullable=False, unique=False,)
    notes = db.Column(db.String(25), nullable=True, unique=False,)  

class Bookmark(db.Model):
    """user favorites"""
    #do i need this table?

    __tablename__ = 'bookmarks'

    bookmark_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            )
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False,
                        unique=False
                        )
    api_recipe_id = db.Column(db.Integer,
                          nullable=False,
                          unique=False,
                          )

#####################################
# Helper Functions

def connect_to_db(app):
    """Connect the database to the Flask app"""

    #need to name database something
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///recipesite'
    app.config["SQLALCHEMY_ECHO"] = False 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    """If this module is run interactively,
    you are able to work with the database directly"""

    from server import app 
    connect_to_db(app)
    print("Connected to database")
    db.create_all()
