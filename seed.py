"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Movie, Rating
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app
import re


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    f = open("seed_data/u.user")

    for row in f:
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Close file
    f.close()

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    # Prevent double-adding movies
    Movie.query.delete()

    # Read u.user file and insert data
    f = open("seed_data/u.item")

    for row in f:
        row = row.rstrip()
        movie_id, title, release_date, _, imdb_url,\
            _, _, _, _, _, _, _, _, _, _,\
            _, _, _, _, _, _, _, _, _ = row.split("|")

        movie = Movie(movie_id=movie_id,
                      title=title,
                      release_at=release_date,
                      imdb_url=imdb_url)

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

    # Close file
    f.close()

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    # Prevent double-adding ratings
    Rating.query.delete()

    # Read u.user file and insert data
    f = open("seed_data/u.data")

    for row in f:
        row = row.rstrip()
        user_id, movie_id, score, timestamp = re.split(r'/t+', row)

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

    # Close file
    f.close()

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
