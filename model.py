"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from correlation import pearson

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Movie(db.Model):
    """Movie of ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id=%s title=%s>" % (self.movie_id, self.title)


class Rating(db.Model):
    """Rating of movie."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))
    movie = db.relationship('Movie', backref=db.backref('ratings', order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating_id=%s movie_id=%s user_id=%s score=%s>" % (self.rating_id, self.movie_id, self.user_id, self.score)

##############################################################################
# Helper functions


def similarity(self_ratings, o_user):

    our_ratings = {}
    for rating in self_ratings:
        our_ratings[rating.movie_id] = rating.score

    paired_ratings = []
    for other_rating in o_user.ratings:
        our_rating = our_ratings.get(other_rating.movie_id)
        if our_rating:
            pair = (our_rating, other_rating.score)
            paired_ratings.append(pair)

    if paired_ratings:
        return pearson(paired_ratings)
    else:
        return 0.0


def get_prediction(user_id, movie_id):
    """Given a user and a movie, returns the predicted ratings"""

    self_ratings = User.query.get(user_id).ratings
    other_ratings = Rating.query.filter_by(movie_id=movie_id).all()

    other_users = [rating.user for rating in other_ratings]

    users_similar = []
    for o_user in other_users:
        sim = similarity(self_ratings, o_user)
        users_similar.append((sim, o_user))

    users_similar = sorted(users_similar, reverse=True)
    top_score = users_similar[0]

    similarity_score, top_user = top_score
    best_rating = Rating.query.filter_by(movie_id=movie_id,
                                         user_id=top_user.user_id).one()

    predicted_rating = best_rating.score * similarity_score

    return int(round(predicted_rating))



def eye_prediction(movie_id):
    """Given a movie, returns the eye's predicted rating"""
    return 1


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
