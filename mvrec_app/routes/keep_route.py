from flask import Blueprint, redirect, url_for, render_template
from mvrec_app import db
from mvrec_app.model.client_movie import KeepMovies
from mvrec_app.utils.youtube_api import youtube_api


bp = Blueprint('keeps',__name__)

@bp.route('/getkeeps', methods=['GET','POST'])
def get_keeps():

    movie_list = []
    for movie in KeepMovies.query.all():
        movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
                                "id":movie.naver_api_info.movie_id,
                                "title_original":movie.naver_api_info.title_original,
                                "image":movie.naver_api_info.image,
                                "pubdate":movie.naver_api_info.pubdate,
                                "youtube_url":youtube_api(movie.naver_api_info.title_original)
                                }
                                )
        

    return redirect(url_for('main.init_keeps'
                            # , _anchor=scroll_idx
                            , movie_list=str(movie_list)))