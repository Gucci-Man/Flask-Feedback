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
        password = form.password.data
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
        session['username'] = new_user.username
        return redirect(f"/users/{username}")

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
            flash(f"Welcome back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def secret(username):
    """Shows info about the user"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    elif session['username'] != username:
        flash("Wrong User!", "danger")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username)
        return render_template("secret.html", user=user, feedback=feedback)


@app.route('/logout')
def logout():
    session.pop('username')
    flash("Goodbye!")
    return redirect('/')