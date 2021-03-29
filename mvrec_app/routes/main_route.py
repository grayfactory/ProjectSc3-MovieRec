from flask import Blueprint, render_template, request
from mvrec_app.model.table_model import Movies
from mvrec_app.model.upload_db import create_table
from mvrec_app.model.queury_db import get_client_rating
from mvrec_app.utils.naver_mv_api import naver_movie_api

bp = Blueprint( 'main', # flask에서 
                __name__  # 이 blueprint를 import 할 때 이름 __name__ 스크립트 파일 이름
                )

@bp.route('/')
def index():
    return render_template('index.html')



@bp.route('/mvrec',methods=['GET','POST'])
def mv_recommend():

    movie_list = request.args.get('movie_list')
    # 지금까지 평가한 영화수
    if len(get_client_rating()) == 0:
        nclientrating = None
    else : nclientrating = len(get_client_rating())
    # print("====="*100)
    # print(movie_list)
    return render_template('movies.html', movie_list=eval(movie_list), nclientrating=nclientrating)



@bp.route('/clientrating',methods=['GET','POST'])
def client_rating():

    movie_list = request.args.get('movie_list')
    print(movie_list, "++"*50)
    if movie_list is None: # 상단의 My Rating으로 이동한 경우
        return render_template('rating.html', movie_list=None, msg=None)
    else : 
        return render_template('rating.html', movie_list=eval(movie_list), msg='on')


@bp.route('/keeps', methods=['GET','POST'])
def init_keeps():

    movie_list = request.args.get('movie_list')

    if movie_list is None: # 상단의 Keep 으로 이동한 경우
        return render_template('keeps.html', movie_list=None, msg=None)
    elif len(eval(movie_list)) == 0:
        return render_template('keeps.html', movie_list=None, msg='empty')
    else :
        return render_template('keeps.html', movie_list=eval(movie_list), msg='on')


