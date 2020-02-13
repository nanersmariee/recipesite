from sqlalchemy import func
from model import Recipe, Ingredient, Recipe_Ingredient, User

from model import connect_to_db, db 
from server import app
from datetime import datetime

def load_recipes():
    """Load recipes from the recipe data file into the database"""

    print("Recipes")

    #prevents duplicate recipe adding
    Recipe.query.delete

    for row in open("seed_data/recipe_data"):
        row = row.rstrip()
        items = row.split("|")

        recipe_id = int(items[0])
        recipe_name = items[1]
        directions = items[2]
        ratings = int(items[3])
        prep_time = items[4]
        cook_time = items[5]
        cuisine = items[6]

        recipe = Recipe(recipe_id=recipe_id,
                        recipe_name=recipe_name,
                        directions=directions,
                        ratings=ratings,
                        prep_time=prep_time,
                        cook_time=cook_time,
                        cuisine=cuisine)

        db.session.add(recipe)

    db.session.commit()

def load_users():
    """Load users from the user data file into database"""

    print("Users")

    #prevents duplicate user adding
    User.query.delete

    for row in open("seed_data/user_data"):
        row = row.rstrip()
        items = row.split("|")

        user_id = items[0]
        email = items[1]
        password = items[2]

        user = User(user_id=user_id,
                    email=email,
                    password=password)

        db.session.add(user)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_recipes()
    load_users()