from flask import Flask, redirect, request, render_template, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import os, requests
from pprint import pformat
import re

from model import connect_to_db, db, Recipe, Ingredient, Recipe_Ingredient, User, Bookmark

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
# app.jinja_env.auto_reload = True 

#Required to use Flask sessions and the debug toolbar
app.secret_key = "adobo"

API_KEY = os.environ['SPOONACULAR_KEY']

@app.route('/')
def begin_at_login():
    """Login Page"""

    return render_template('login-page.html')

@app.route('/login', methods=['POST'])
def authenticate_user():
    """authenticate user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user_in_system = User.query.filter_by(email=email).first()
    password_in_system = user_in_system.password 
   

    if not user_in_system:
        flash('User does not exist')
        return redirect('/')
    elif password_in_system == password:
        session['current_user'] = user_in_system.user_id
        session['current_user_name'] = user_in_system.user_name 
        flash('Successfully Logged In, Homie!')
        return redirect('/main-page')
    else:
        flash('Sorry Dude, Login Failed')
        return redirect('/')

@app.route('/logout')
def logout():
    """Log out"""

    del session['current_user']
    flash('Logged Out')
    return redirect('/')

@app.route('/new-user', methods=['GET'])
def show_new_user_form():
    """Shows a form to add a new user's information"""

    return render_template('new-user.html')

@app.route('/new_user', methods=['POST'])
def enter_new_user_data():
    """Enters new user information"""

    user_name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user_in_db = User.query.filter_by(email=email).first()

    if not user_in_db:
        user = User(user_name=user_name,
                    email=email,
                    password=password)
        flash('Username Created, Time to Eat!')
        db.session.add(user)
        db.session.commit()
    else:
        flash('User already exists')
    return redirect('/')

@app.route('/main-page')
def continue_to_main():
    """Goes to main page after login"""

    return render_template('main-page.html')

@app.route('/bookmark', methods=['POST'])
def add_bookmark():
    """user can bookmark a recipe"""

    content = request.get_json()
    api_recipe_id = content.get('api_recipe_id')
    user_id = session['current_user']
    
    # ingredients = (request.args.get('ingredients'))

    bookmark = Bookmark(user_id=user_id,
                        api_recipe_id=api_recipe_id,
                        )
    db.session.add(bookmark)
    db.session.commit()
    print('adding a bookmark')

    return jsonify()

@app.route('/bookmark', methods=['DELETE'])
def remove_bookmark():
    """removes a bookmark of a recipe"""

    content = request.get_json()
    api_recipe_id = content.get('api_recipe_id')
    user_id = session['current_user']

    bookmark = Bookmark.query.filter_by(user_id=user_id, api_recipe_id=api_recipe_id).first()
    
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()

    print('removing a bookmark')

    return ''
    

@app.route('/my-bookmarks')
def get_my_bookmarks_list():
    """Show a list of user's bookmarks"""

    bookmark = Bookmark.query.all()
    return render_template('bookmarks_list.html',
                            bookmark=bookmark)

@app.route('/ingredients')
def show_ingredients_form():
    """search recipes by entering ingredients in form"""

    return render_template('search-form.html')

@app.route('/ingredients/search')
def search_recipes():
    """Search recipes by ingredient"""

    ingredients = (request.args.get('ingredients')).title()
    num_recipes =request.args.get('num_recipes')
    print(ingredients)
    print(num_recipes)

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        })
    
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients'
    

    payload = {'apiKey': API_KEY,
               'ingredients': ingredients,
               'num_recipes': 25}

    response = requests.get(url, 
                            params=payload, 
                            headers=headers)

    data = response.json()

    return render_template('search-results.html',
                            data=data,
                            ingredients=ingredients)

@app.route('/recipes/<api_recipe_id>')
def show_recipe_details(api_recipe_id):

    api_recipe_id = api_recipe_id
    TAG_RE = re.compile(r'<[^>]+>')

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(api_recipe_id)
    print(url)

    payload = {'apiKey': API_KEY,
               'id': api_recipe_id}

    response = requests.get(url,
                            params=payload,
                            headers=headers)

    data = response.json()
    
    
    summary = TAG_RE.sub('', data.get('summary', '[NA]'))
    preparation_time = data.get('preparationMinutes', '[NA]')
    cooking_time = data.get('cookingTime', '[NA]')
    likes = data.get('aggregateLikes', '[NA]')
    serving_size = data.get('servings', '[NA]')
    diet = data.get('diets', '[NA]')
    dish_type = data.get('dishTypes', '[NA]')
    cuisine = data.get('cuisines', '[NA]')
    api_recipe_title = data.get('title', '[NA]')
    recipe_image = data['image']
    
    

    # if not summary:
    #     summary = "NA"
    # if "preparationMinutes" not in data:
    #     preparation_time = "NA"


    return render_template('recipe-details.html',
                           data=data,
                           api_recipe_id=api_recipe_id,
                           summary=summary,
                           preparation_time=preparation_time,
                           cooking_time=cooking_time,
                           likes=likes,
                           serving_size=serving_size,
                           diet=diet,
                           dish_type=dish_type,
                           cuisine=cuisine,
                           api_recipe_title=api_recipe_title,
                           recipe_image=recipe_image)


@app.route('/recipes')
def recipe_list():
    """Show a list of user recipes"""

    recipes = Recipe.query.all()
    return render_template('recipe_list.html',
                            recipes=recipes)

@app.route('/enter-recipe', methods=['GET'])
def enter_recipe():
    """Shows a form for a user to enter a recipe"""

    return render_template('enter_recipe.html')

@app.route('/enter-recipe', methods=['POST'])
def recipe_entered():
    """Adds a recipe that a user entered into the recipe directory"""

    recipe_name = request.form.get('recipe_name')
    directions = request.form.get('directions')
    prep_time = request.form.get('prep-time')
    cook_time = request.form.get('cook-time')
    cuisine = request.form.get('cuisine')

    recipe = Recipe(recipe_name=recipe_name,
                    directions=directions,
                    prep_time=prep_time,
                    cook_time=cook_time,
                    cuisine=cuisine)

    db.session.add(recipe)
    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    # DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0")

#ignore me
#<a href="/recipes/{{ data[0]['id'] }}">