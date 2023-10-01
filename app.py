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

# TODO - Show all feedback for that user
# TODO - Display a link to form to edit the feedback
# TODO - Have a button to delete the feedback
# Only user can do these
@app.route('/users/<username>')
def secret(username):
    """Shows info about the user"""

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    elif session['username'] != username:
        flash("Wrong User! Please login.", "danger")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username)
        return render_template("secret.html", user=user, feedback=feedback)
    
# TODO - checks if this works 
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete user and all their feedback"""

    # Checks if user is login and is correct user
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    elif session['username'] != username:
        flash("Wrong User!", "danger")
        return redirect('/login')
    
    # Delete any feedback the user may have first
    feedback = Feedback.query.filter_by(username=username).all()

    if len(feedback) != 0:
        for feed in feedback:
            Feedback.query.filter_by(id=feed.id).delete()
            db.session.commit()
    
    # Deleting the user and remove from session
    User.query.filter_by(username=username).delete()
    db.session.commit()
    session.pop('username')

    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Display a form to add feedback. Only user can see this."""

    # Checks if user is login and is correct user
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    elif session['username'] != username:
        flash("Wrong User!", "danger")
        return redirect('/login')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.title.data
        new_feed = Feedback(title=title, content=content, username=username)
        db.session.add(new_feed)
        db.session.commit()
        flash('Feedback Created!', 'success')
        return redirect(f'/users/{username}') # Redirect to user profile after adding feedback
    
    return render_template('add_feedback.html', form=form, username=username)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete user's feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user

    #Checks if user is login and is correct user
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    elif session['username'] != user.username:
        flash("Wrong User! You don't have permission to delete that feedback!", "danger")
        return redirect('/login')
    
    # Deleting feedback then redirect back to user profile
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f"/users/{user.username}")



@app.route('/logout')
def logout():
    session.pop('username')
    flash("Goodbye!")
    return redirect('/')