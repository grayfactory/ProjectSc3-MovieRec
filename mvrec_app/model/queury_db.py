from mvrec_app.model.table_model import RatingUsers, Movies
from mvrec_app.model.client_movie import RenderMovies, RatingClient, NotSeenClient, NaverMovies, KeepMovies
from mvrec_app.model import upload_db
from mvrec_app import db
from mvrec_app.utils.naver_mv_api import naver_movie_api
# import numpy as np
import random


def get_init_movies(genre=None, n_select=20):
    """
    초기 추천 영화 쿼리 
    genre=장르, n_select=몇개
    return = Moivies 인스턴스들의 리스트
    """
    # 장르 filter & 랜덤으로 20개
    if genre is not None:
        q_movies = [q for q in Movies.query.filter(Movies.genre.contains(genre)).all()]
    else :
        q_movies = [q for q in Movies.query.all()]

    # 필터 여러개
    # q_movies = [q for q in Movies.query.filter(Movies.genre.contains('Action'))
    # .filter(Movies.weight_rating >=4).all()]

    return random.sample(q_movies, n_select)


def store_render_movies(q_movies):
    """
    20개씩 쿼리한 영화의 list를 동일하게 유지하면서
    랜더링해주기 위해서 작성됨 
    """
    for movies in q_movies:
        naver_id = NaverMovies.query.filter(NaverMovies.movie_id == movies.movie_id).one_or_none()
        record = RenderMovies(movie_id=movies.movie_id, naver_id=naver_id.id)
        # print(record)
        db.session.add(record)
    db.session.commit()
    # for m in RenderMovies.query.all():
    #     print(m)
    

def store_client_rating(score, movie_id):
    """
    클라이언트의 rating 점수를 commit
    movie_id : Movies table의 PK id 로저장됨
    """
    movie_id = int(movie_id)
    # 중복 방지
    isin_Rating = RatingClient.query.filter(RatingClient.movie_id == movie_id).one_or_none()
    isin_NotSee = NotSeenClient.query.filter(NotSeenClient.movie_id == movie_id).one_or_none()

    if (isin_Rating is None and isin_NotSee is None):
        if score == '9':
            new_record = NotSeenClient(movie_id=movie_id)
        else :
            naver_id = NaverMovies.query.filter(NaverMovies.movie_id == movie_id).one_or_none()
            new_record = RatingClient(client_rating=int(score), movie_id=movie_id, naver_id=naver_id.id)
        db.session.add(new_record)
        db.session.commit()

def get_client_rating():
    return RatingClient.query.all()

def get_render_movies():
    return RenderMovies.query.all()
    # return db.session.query(db.func.distinct(RenderMovies.movie_id)).all()

def delete_records(q_movies):
    for q in q_movies:
        db.session.delete(q)

def reset_client_db():
    """
    home 화면의 시작하기와 함께
    기존에 client가 저장한 db record를 삭제
    """
    q_movies = RenderMovies.query.all()
    if q_movies is not None:
        delete_records(q_movies)
        
    q_movies = RatingClient.query.all()
    if q_movies is not None:
        delete_records(q_movies)  
     
    q_movies = NotSeenClient.query.all()
    if q_movies is not None:
        delete_records(q_movies) 
    db.session.commit()    

    q_movies = KeepMovies.query.all()
    if q_movies is not None:
        delete_records(q_movies)
    db.session.commit()

def reset_render_movies():
    q_movies = RenderMovies.query.all()
    if q_movies is not None:
        delete_records(q_movies)

def store_sim_user_movies(sim_user, n_limit=10):
    q_movies = RatingUsers.query.filter(RatingUsers.user_id == sim_user).\
        order_by(RatingUsers.rating.desc()).\
            limit(n_limit).all()
    
    for movie in q_movies:

        isin_Rating = RatingClient.query.filter(RatingClient.movie_id == movie.movie_id).one_or_none()
        isin_NotSee = NotSeenClient.query.filter(NotSeenClient.movie_id == movie.movie_id).one_or_none()
        isin_keep = KeepMovies.query.filter(KeepMovies.movie_id == movie.movie_id).one_or_none()

        if (isin_Rating is None and isin_NotSee is None and isin_keep is None):

            m = Movies.query.filter(Movies.movie_id==movie.movie_id).one_or_none()
            movie_list = naver_movie_api([{'title':m.title, 'id':m.movie_id}])
            # 새로 추천하는 영화의 naver api version 저장
            # print(movie_list)
            store_naver_api_movies(movie_list)
            
            naver_id = NaverMovies.query.filter(NaverMovies.movie_id == movie.movie_id).one_or_none()
            record = RenderMovies(movie_id=movie.movie_id, naver_id=naver_id.id)

            db.session.add(record)
    # db.session.commit()


def store_naver_api_movies(movie_list):

    # naver api 에서 긁은 정보 저장 (API 요청은 한번만 하기위해)

    for movie in movie_list:
        isin_Naver = NaverMovies.query.filter(NaverMovies.movie_id == int(movie['id'])).one_or_none()
        if isin_Naver is None:
            record = NaverMovies(title_original=movie['title_original']
                                ,title_kr=movie['title_kr']
                                ,pubdate=movie['pubdate']
                                ,image=movie['image']
                                ,actor=movie['actor']
                                ,director=movie['director']
                                ,movie_id=int(movie['id'])
                                )
            db.session.add(record)
    db.session.commit()

def store_keep_movie(movie_id):
    is_keep = KeepMovies.query.filter(KeepMovies.movie_id == int(movie_id)).one_or_none()
    if is_keep is None:
        q_naver = NaverMovies.query.filter(NaverMovies.movie_id == int(movie_id)).one_or_none()

        record = KeepMovies(movie_id=int(movie_id), naver_id=q_naver.id)
        db.session.add(record)
        db.session.commit()

def get_naver_api_movies(movie_id_list):

    q_movies = NaverMovies.query.filter(NaverMovies.movie_id.in_(movie_id_list)).all()

    return q_movies


