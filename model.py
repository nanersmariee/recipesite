from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


db = SQLAlchemy()


class Recipe(db.Model):
    """individual recipes"""

    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True,
                          )
    directions = db.Column(db.String(100), nullable=False, unique=False,)
    ratings = db.Column(db.Integer, nullable=True, unique=False,)
    prep_time = db.Column(db.Integer, nullable=False, unique=False,)
    cook_time = db.Column(db.Integer, nullable=False, unique=False,)
    cuisine = db.Columng(db.String(25), nullable=False, unique=False,)
    #can i put multiple cuisines into this column, Ex: Asian, Filipino

class Ingredent(db.Model):
    """Individual ingredients from a comprehensive list"""

    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=True,
                              )
    name = db.Column(db.String(25), nullable=False, unique=True,)

class Recipe_Ingredient(db.Model):
    """Ingredients from Recipes"""

    __tablename__ = recipe_ingredients

    recipe_ingredients_id = db.Column(db.Integer,
                                      primary_key=True,
                                      autoincrement=True,
                                      )
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredients.ingredient_id')
                              nullable=False,
                              unique=True,
                              )
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipes.recipe_id'),
                          nullable=False,
                          unique=False,
                          )
    #check for uniques and nullables if they make sense

class User(db.Model):
    """individual users"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        )
    email = db.Column(db.String(25), nullable=False, unique=True,)
    bookmarks = db.Column(db.String(24), nullable=True, unique=True,)


class Bookmark(db.Model):
    """user favorites"""
    #do i need this table?

    __tablename__ = bookmarks

    bookmark_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            )
    recipe_id = db.Column(db.Integer,db.ForeignKey('recipes.recipe_id'),
                          nullable=False,
                          unique=True,
                          )






#####################################
# Helper Functions

def connect_to_db(app):
    """Connect the database to the Flask app"""

    #need to name database something
    #app.config["SQLALCHEMY_DATABASE_URI"] = 'postegresql:///'
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
