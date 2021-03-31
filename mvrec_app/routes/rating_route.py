from flask import Blueprint, request, redirect, url_for, Response
from mvrec_app.model.client_movie import RatingClient, NotSeenClient, RenderMovies, NaverMovies
from mvrec_app.model.table_model import RatingUsers, Movies
from mvrec_app import db
from mvrec_app.model.queury_db import get_init_movies, store_client_rating, reset_render_movies, store_sim_user_movies, store_keep_movie
from mvrec_app.model.queury_db import store_render_movies, get_render_movies, reset_client_db, store_naver_api_movies, get_client_rating
from mvrec_app.utils.main_funcs import cosine_sim, movie_list_dict
from mvrec_app.utils.naver_mv_api import naver_movie_api


bp = Blueprint('ratings',__name__)

@bp.route('/rating', methods=['POST'])
def add_movie_rating():
    
    if request.method == 'POST': 
        score = request.form.get('submit',None)
        movie_id = request.form.get('title',None) # Movies movie_id
        scroll_idx = request.form.get('scrollindex', None)
        keep_idx = request.form.get('keep',None)
        print(score, movie_id, scroll_idx,keep_idx,'===='*30)

    if keep_idx is not None:
        store_keep_movie(movie_id)

    # rating 정보를 저장
    if score is not None:
        store_client_rating(score, movie_id)

    # movie_list = []
    # duplicats = []
    # # 현재 랜더된 영화를 유지하면서 redirect
    # for movie in get_render_movies(): 
    #     duplicats.append(movie.rendered_movies.movie_id)
    #     # print(duplicats, movie.rendered_movies.movie_id)
    #     if duplicats.count(movie.rendered_movies.movie_id) > 1:
    #         continue
    #     else :
    #         # print(movie, '++'*50)
    #         ## movie_list = "image", "title_kr", "pubdate", "title_original"
    #         movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
    #                             "id":movie.naver_api_info.movie_id,
    #                             "title_original":movie.naver_api_info.title_original,
    #                             "image":movie.naver_api_info.image,
    #                             "pubdate":movie.naver_api_info.pubdate
    #                             }
    #                             )

    # print('here'*100)
    # print(movie_list)

    # mvrec page에서 평점을 누르면 redirect
    return redirect(url_for('main.mv_recommend', _anchor=scroll_idx, movie_list=None))


@bp.route('/getstart')
def init_first_movies():

    # 기존에 존재하는 client table의 recode를 모두 삭제
    reset_client_db()

    # 초기 20개 랜덤으로 추천
    # genre 필터를 고를 수 있게 수정
    q_movies = get_init_movies(n_select=20)

    movie_list = []
    for movie in q_movies:
        movie_list.append({"title":movie.title, "id":movie.movie_id})  # Movie table에서 movie_id 로넘겨주고

    movie_list_api = naver_movie_api(movie_list)
    store_naver_api_movies(movie_list_api)

    store_render_movies(q_movies)

    movie_id_list = [mid['id'] for mid in movie_list_api]
    # get url이 너무 길어서 heroku에서 작동하지 않음 id만 넘기기

    return redirect(url_for('main.mv_recommend', movie_list=str(movie_id_list)))

@bp.route('/getrec')
def init_rec_movies():

    join_db = db.session.query(RatingUsers.user_id, RatingUsers.movie_id, RatingUsers.rating).\
        join(RatingClient, RatingUsers.movie_id==RatingClient.movie_id).all()

    client = [(0, q.movie_id, q.client_rating) for q in RatingClient.query.order_by(RatingClient.movie_id).distinct()]
    # 유사한 유저 top 3 리스트
    sim_users = cosine_sim(join_db, client)
    
    # 1 RenderMovies를 비운다
    reset_render_movies()

    # 2 3명의 상위 10 영화를 RenderMovies에 넣는데 중복을 막으면서 넣는다.
    # n_linit defult : top 10
    for user in sim_users:
        store_sim_user_movies(user)

    # movie_list = []
    # duplicats = []
    # # 현재 랜더된 영화를 유지하면서 redirect
    # for movie in get_render_movies(): 
    #     # print(movie, "=="*50)
    #     duplicats.append(movie.rendered_movies.movie_id)
    #     # print(duplicats, movie.rendered_movies.movie_id)
    #     if duplicats.count(movie.rendered_movies.movie_id) > 1:
    #         continue
    #     else :
    #         # print(movie, movie.naver_id,'++'*50)
    #         ## movie_list = "image", "title_kr", "pubdate", "title_original"
    #         movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
    #                             "id":movie.naver_api_info.movie_id,
    #                             "title_original":movie.naver_api_info.title_original,
    #                             "image":movie.naver_api_info.image,
    #                             "pubdate":movie.naver_api_info.pubdate
    #                             }
    #                             )

    movie_list = len(get_client_rating())
    return redirect(url_for('main.mv_recommend', movie_list=str(movie_list)))


@bp.route('/getmyrating')
def init_rating_table():
    
    return redirect(url_for('main.client_rating', movie_list=str([1,2,3])))


