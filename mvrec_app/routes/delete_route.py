from flask import Blueprint, redirect, url_for
from mvrec_app import db
from mvrec_app.model.client_movie import RatingClient, KeepMovies

bp = Blueprint('delete',__name__)

@bp.route('/delete/')
@bp.route('/delete/<int:movie_id>')
def delete_rating(movie_id=None):
    
    q_movie = RatingClient.query.filter(RatingClient.movie_id==movie_id).one_or_none()
    print(q_movie,'hi?'*50)    
    if q_movie is None:
        return redirect(url_for('ratings.init_rating_table'))
    else :
        db.session.delete(q_movie)
        db.session.commit()
        return redirect(url_for('ratings.init_rating_table'))



@bp.route('/delete/keep/<int:movie_id>')
def delete_keep(movie_id=None):
    
    q_movie = KeepMovies.query.filter(KeepMovies.movie_id==movie_id).one_or_none()
    print(q_movie,'hi?'*50)    
    if q_movie is None:
        return redirect(url_for('keeps.get_keeps'))
    else :
        db.session.delete(q_movie)
        db.session.commit()
        return redirect(url_for('keeps.get_keeps'))