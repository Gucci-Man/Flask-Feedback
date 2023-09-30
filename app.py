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
        username = form.username.data
        password = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form)
        return redirect("/secret")

    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login form"""

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!")
            return redirect('/secret')
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template('login.html', form=form)




@app.route('/secret')
def secret():
    """Secret view once user login/register"""

    return render_template("secret.html")