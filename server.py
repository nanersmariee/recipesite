from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import Strict Undefined


app = Flask(__name__)
# app.jinja_env.undefined = StrictUndefined
# app.jinja_env.auto_reload = True

#Required to use Flask sessions and the debug toolbar
app.secret_key = "adobo"

@app.route('/')
def begin_homepage():
    """Homepage"""

    return render_template