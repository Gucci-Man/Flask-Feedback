from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import *
from forms import *
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.app_context().push()
    
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "BATMANISAWESOME!!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    """Redirect to /register"""

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show form to register a user"""

    form = UserForm()
    if form.validate_on_submit():
        """take data"""
        username = form.username.data
        password = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name,last_name=last_name)
        db.session.add(user)
        db.session.commit()

        return redirect("/secret")

    return render_template("register.html", form=form)