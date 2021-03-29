from mvrec_app import db

class RatingClient(db.Model):
    __tablename__ = "rating_client"

    id = db.Column(db.Integer(), primary_key=True)
    client_rating = db.Column(db.Integer())
    # movie id
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))
    naver_id = db.Column(db.Integer(), db.ForeignKey('naver_movies.id'))

    # rated_users = db.relationship("RatingUsers", backref='ratingclient', lazy=True)
    naver_api_info = db.relationship("NaverMovies", backref='clientrating', lazy=True)

    def __repr__(self):
        return f"< id: {self.movie_id}, rating: {self.client_rating} >"


class NotSeenClient(db.Model):
    __tablename__ = "notseen_client"

    id = db.Column(db.Integer(), primary_key=True)

    movie_id = db.Column(db.Integer())

# 첫 번째 20개 부터 시작해서 지금까지 가지고온 영화를 담고있어서
# 랜더 template할때 계속 랜덤하게 바뀌지 않도록
class RenderMovies(db.Model):
    __tablename__ = "render_movies"

    id = db.Column(db.Integer(), primary_key=True)
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))
    naver_id = db.Column(db.Integer(), db.ForeignKey('naver_movies.id'))

    rendered_movies = db.relationship("Movies", back_populates="rendered", lazy=True)

    naver_api_info = db.relationship("NaverMovies", backref='rendered', lazy=True)

    def __repr__(self):
        return f"< movie_id: {self.movie_id} >"

    # rendered로 relationship 연결해주었음

class NaverMovies(db.Model):
    __tablename__ = "naver_movies"

    id = db.Column(db.Integer(), primary_key=True)

    title_original = db.Column(db.String())
    title_kr = db.Column(db.String())
    pubdate = db.Column(db.String())
    image = db.Column(db.String())
    actor = db.Column(db.String())
    director = db.Column(db.String())

    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))

    def __repr__(self):
        return f"< title: {self.title_kr} ({self.pubdate}) >"
    
class KeepMovies(db.Model):
    __tablename__ = "keep_movies"

    id = db.Column(db.Integer(), primary_key=True)

    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))
    naver_id = db.Column(db.Integer(), db.ForeignKey('naver_movies.id'))

    naver_api_info = db.relationship("NaverMovies", backref='keeps', lazy=True)
    rendered_movies = db.relationship("Movies", backref="keeps", lazy=True)