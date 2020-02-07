from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
# app.jinja_env.undefined = StrictUndefined
# app.jinja_env.auto_reload = True

#Required to use Flask sessions and the debug toolbar
app.secret_key = "adobo"

@app.route('/')
def begin_homepage():
    """Homepage"""
    # put a recipe into the db by hand
    # query database for a recipe 
    # create a template to show the recipe 
    # pass recipe info down to template 
    return render_template('homepage.html')


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")