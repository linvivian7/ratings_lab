"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, request, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

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


@app.route('/login')
def log_in():

    return render_template('sign_in.html')


@app.route('/process_login', methods=["POST"])
def process_login():

    email = request.form.get('email')
    # check if user exists

    try:
        User.query.filter_by(email=email).one()
    except:
        flash("A new user has been created")
        user = User(email=email)

                user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Close file
    f.close()

    # Once we're done, we should commit our work
    db.session.commit()

    # check if password correct
        return redirect('/')


        return redirect('/login')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
