from mvrec_app import db

class RatingUsers(db.Model):
    __tablename__ = "rating_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    rating = db.Column(db.Float())
    
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))
    
    def __repr__(self):
        return f"< user: {self.user_id}, movie id: {self.movie_id}, rating: {self.rating} >"


class Movies(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer(), primary_key=True)
    movie_id = db.Column(db.Integer())
    title = db.Column(db.String())
    genre = db.Column(db.String())
    weight_rating = db.Column(db.Float())

    rendered = db.relationship("RenderMovies", back_populates="rendered_movies", lazy=True)
    # rated_users = db.relationship("RatingUsers", back_populates="rating_movie", lazy=True)

    def __repr__(self):
        return f"< movie id: {self.movie_id}, title: {self.title}, w_rating: {self.weight_rating} >"

