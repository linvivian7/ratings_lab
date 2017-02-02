CREATE TABLE ratings (
    rating_id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies NOT NULL,
    user_id INTEGER REFERENCES users NOT NULL,
    score INTEGER NOT NULL,
    UNIQUE(movie_id, user_id)
    );