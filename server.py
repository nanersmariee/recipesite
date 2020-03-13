from flask import Flask, redirect, request, render_template, session, flash, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import os, requests
from pprint import pformat
import re, sys 

from model import connect_to_db, db, My_Recipe, User, Bookmark

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

    user = User.query.filter_by(email=email).first()
    # password_in_system = user.password 
   

    if not user:
        flash('User does not exist')
        return redirect('/')

    if user.password != password:
        flash('Sorry Dude, Login Failed')
        return redirect('/')

    session['current_user'] = user.user_id
    session['current_user_name'] = user.user_name 
    
    flash('Successfully Logged In, Homie!')
    return redirect('/main-page')

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
    

@app.route('/my-bookmarks/<user_id>')
def get_my_bookmarks_list(user_id):
    """Show a list of user's bookmarks"""

    user_id = user_id
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    bookmark_titles = {} 

    for bookmark in bookmarks:
        api_recipe_id = bookmark.api_recipe_id
    
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

        bookmark_titles[api_recipe_id] = data['title']

    return render_template('bookmarks-list.html',
                            bookmarks=bookmarks,
                            data=data,
                            bookmark_titles=bookmark_titles)

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
    readyInMinutes = data.get('readyInMinutes', '[NA]')
    likes = data.get('aggregateLikes', '[NA]')
    serving_size = data.get('servings', '[NA]')
    diet = data.get('diets', '[NA]')
    dish_type = data.get('dishTypes', '[NA]')
    cuisine = data.get('cuisines', '[NA]')
    api_recipe_title = data.get('title', '[NA]')
    instructions = data.get('instructions', '[NA]')
    recipe_image = data['image']
    recipe_aisle = data.get('aisle', '[NA]')
    
    return render_template('recipe-details.html',
                           data=data,
                           api_recipe_id=api_recipe_id,
                           summary=summary,
                           readyInMinutes=readyInMinutes,
                           likes=likes,
                           serving_size=serving_size,
                           diet=diet,
                           dish_type=dish_type,
                           cuisine=cuisine,
                           api_recipe_title=api_recipe_title,
                           instructions=instructions,
                           recipe_image=recipe_image,
                           recipe_aisle=recipe_aisle)

@app.route('/nutrition/<api_recipe_id>')
def show_nutrition(api_recipe_id):
    """show nutrition of a recipe by recipe id"""

    api_recipe_id = api_recipe_id
    print(api_recipe_id)

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });
    # url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/nutritionWidget".format(api_recipe_id)
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/nutritionWidget.json".format(api_recipe_id)
    print(url)

    payload = {'apiKey': API_KEY,
               'id': api_recipe_id}

    response = requests.get(url,
                            params=payload,
                            headers=headers)
    data = response.json()

    return render_template('nutrition.html',
                            data=data,
                            api_recipe_id=api_recipe_id)


def get_name(api_recipe_id):

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(api_recipe_id)
    

    payload = {'apiKey': API_KEY,
               'id': api_recipe_id}

    response = requests.get(url,
                            params=payload,
                            headers=headers)

    data = response.json()
    
    return data.get('title', '[NA]')

@app.route('/similar-recipes/<api_recipe_id>')
def get_similar_recipes(api_recipe_id):
    
    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    info_url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(api_recipe_id)
    

    payload = {'apiKey': API_KEY,
               'id': api_recipe_id}

    info_response = requests.get(info_url,
                    params=payload,
                    headers=headers)

    info_data = info_response.json()
    
    api_recipe_title = info_data.get('title')
    print(api_recipe_title)

    
    similar_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/similar".format(api_recipe_id)


    similar_response = requests.get(similar_url,
                            params=payload,
                            headers=headers)
    similar_data = similar_response.json()

    print(api_recipe_title)

    return render_template('similar-recipes.html',
                            data=similar_data,
                            title=api_recipe_title)


@app.route('/add-recipe-url-form')
def show_form_for_url():
    """Shows form to enter a url"""

    return render_template('add-recipe-url-form.html')


@app.route('/add-recipe')
def add_recipe_url():
    """Add a recipe url"""

    url_upload=request.args.get('url')
    TAG_RE = re.compile(r'<[^>]+>')

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract'
    print(url)

    payload = {'apiKey': API_KEY,
               'url': url_upload}

    response = requests.get(url,
                            params=payload,
                            headers=headers)

    data = response.json()
    
    summary = data.get('summary', '[NA]')
    #summary = TAG_RE.sub('', data.get('summary', '[NA]'))
    cookingMinutes = data.get('cookingMinutes', '[NA]')
    preparationMinutes = data.get('preparationMinutes', '[NA]')
    likes = data.get('aggregateLikes', '[NA]')
    serving_size = data.get('servings', '[NA]')
    diet = data.get('diets', '[NA]')
    dish_type = data.get('dishTypes', '[NA]')
    cuisine = data.get('cuisines', '[NA]')
    api_recipe_title = data.get('title', '[NA]')
    instructions = data.get('instructions', '[NA]')
    recipe_image = data['image']
    recipe_aisle = data.get('aisle', '[NA]')
    
    return render_template('add-recipe-url.html',
                           data=data,
                           summary=summary,
                           preparationMinutes=preparationMinutes,
                           cookingMinutes=cookingMinutes,
                           likes=likes,
                           serving_size=serving_size,
                           diet=diet,
                           dish_type=dish_type,
                           cuisine=cuisine,
                           api_recipe_title=api_recipe_title,
                           instructions=instructions,
                           recipe_image=recipe_image)

    render_template('add-recipe-url.html')

@app.route('/wine-rec')
def search_wine():
    """Search form for wine"""

    return render_template('wine-rec-form.html')

@app.route('/wine-results')
def get_wine_rec():

    """Get a wine recommendation"""

    wine = (request.args.get('wine')).title()

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/wine/recommendation"

    payload = {'apiKey': API_KEY,
               'wine': wine}

    response = requests.get(url,
                            params=payload,
                            headers=headers)

    data = response.json()
    print(data)
    return render_template('wine-recs-results.html',
                            wine=wine,
                            data=data)

@app.route('/wine-pair')
def search_wine_pair():
    """Search form for wine pairing"""

    return render_template('wine-pair-form.html')

@app.route('/wine-pair-results')
def get_wine_pair():

    """Get a wine pairing"""

    food = (request.args.get('food')).title()

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/wine/pairing"

    payload = {'apiKey': API_KEY,
               'food': food}

    response = requests.get(url,
                            params=payload,
                            headers=headers)

    data = response.json()
    print(data)
    return render_template('wine-pair-results.html',
                            food=food,
                            data=data)

@app.route('/joke')
def tell_joke():
    """Get a random joke"""

    headers = ({
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
        });

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/jokes/random"

    payload = {'apiKey': API_KEY}

    response = requests.get(url,
                            params=payload,
                            headers=headers)

    data = response.json()

    return render_template('tell-joke.html',
                           data=data)


@app.route('/my-recipes')
def recipe_list():
    """Show a list of user recipes"""

    user_id = session['current_user']
    recipes = My_Recipe.query.all()
    return render_template('my-recipes-list.html',
                            recipes=recipes,
                            user_id=user_id)

@app.route('/my-recipes/<recipe_id>')
def get_my_recipe_details(recipe_id):
    """Show recipe details from user's recipe"""

    recipe_id = recipe_id
    recipe = My_Recipe.query.filter_by(recipe_id=recipe_id).first()


    print(recipe_id)
    print(recipe)
    

    return render_template('my-recipe-details.html',
                            recipe=recipe,
                            recipe_id=recipe)

@app.route('/edit-my-recipe/<recipe_id>', methods=['GET'])
def edit_my_recipe(recipe_id):
    """allows user to edit their own recipe"""
    print("***********************")
    print()
    print(recipe_id)

    print()
    print('***********************')
    recipe = My_Recipe.query.filter_by(recipe_id=recipe_id).first()


    render_template('edit-my-recipe.html')

@app.route('/enter-recipe', methods=['GET'])
def enter_recipe():
    """Shows a form for a user to enter a recipe"""

    return render_template('enter_recipe.html')

@app.route('/enter-recipe', methods=['POST'])
def recipe_entered():
    """Adds a recipe that a user entered into the recipe directory"""
    
    user_id = session['current_user']
    recipe_name = request.form.get('recipe_name')
    ingredients = request.form.get('ingredients')
    directions = request.form.get('directions')
    prep_time = request.form.get('prep-time')
    cook_time = request.form.get('cook-time')
    cuisine = request.form.get('cuisine')

    recipe = My_Recipe(recipe_name=recipe_name,
                    ingredients=ingredients,
                    directions=directions,
                    prep_time=prep_time,
                    cook_time=cook_time,
                    cuisine=cuisine,
                    user_id=user_id)

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