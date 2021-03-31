from flask import Blueprint, redirect, url_for, render_template
from mvrec_app import db
from mvrec_app.model.client_movie import KeepMovies
from mvrec_app.utils.youtube_api import youtube_api


bp = Blueprint('keeps',__name__)

@bp.route('/getkeeps', methods=['GET','POST'])
def get_keeps():

    movie_list = [q_movies.movie_id for q_movies in KeepMovies.query.all()]
        
    return redirect(url_for('main.init_keeps'
                            # , _anchor=scroll_idx
                            , movie_list=str(movie_list)))