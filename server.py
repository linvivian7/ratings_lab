"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, request, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """List of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<userid>')
def user_info(userid):
    """Shows available info for given user"""

    user = User.query.filter_by(user_id=userid).one()
    ratings = Rating.query.filter_by(user_id=userid).all()
    mv_ratings = []

    for rating in ratings:
        movie = Movie.query.filter_by(movie_id=rating.movie_id).one()
        mv_ratings.append((movie.title, rating.score))

    return render_template('user.html', user=user, ratings=mv_ratings)


@app.route('/login')
def log_in():
    """Log in page"""

    return render_template('sign_in.html')


@app.route('/process_login', methods=["POST"])
def process_login():
    """Processes login and adds new users"""

    email = request.form.get('email')
    # check if user exists
    password = request.form.get('password')

    try:
        user = User.query.filter_by(email=email).one()
    # only throws exception if there is no entry in the database
    # if there are too many, the user is out of luck
    except NoResultFound:
        flash("A new user has been created")

        user = User(email=email, password=password)
        db.session.add(user)

        session['user'] = user.user_id
        db.session.commit()

        html = '/users/' + str(user.user_id)
        return redirect(html)

    if password == user.password:

        flash("Logged in!")
        session['user'] = user.user_id
        html = '/users/' + str(user.user_id)
        return redirect(html)

    flash("Your email or password is incorrect.")
    return redirect('/login')


@app.route('/logout')
def logout():
    """Logs out the user"""

    session.pop('user')
    flash("You have been logged out.")
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
