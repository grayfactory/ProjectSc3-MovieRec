import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from mvrec_app.utils.youtube_api import youtube_api

def cosine_sim(join_db, client_db, ratio=0.6):

    """
    RatingUser, RatingClient 의 join 쿼리 결과를 받아서 코사인 유사도를 계산
    ratio parameter로 User의 null값을 어느정도까지 허용할지 조절

    input 
    join_db : RatingUser join 쿼리 결과 tuple (RatingUsers.user_id, RatingUsers.movie_id, RatingUsers.rating)
    client_db : RatingClient 쿼리 결과 tuple 

    return : user_id list 가장 유사한 3명
    """


    # User pivot
    df_join = pd.DataFrame(join_db, columns=['user_id','movie_id','rating'])
    idx = df_join.pivot(index='user_id',columns='movie_id', values='rating').isnull().sum(axis=1) <= len(client_db)*ratio
    df_pivot = df_join.pivot(index='user_id',columns='movie_id', values='rating').loc[idx]
    # client pivot
    df_client = pd.DataFrame(client_db, columns=['user_id','movie_id','rating']).pivot(index='user_id',columns='movie_id', values='rating')

    df = pd.concat([df_client, df_pivot])
    df = df.fillna(0)

    # print(df)

    # similarity 계산
    sim_scores = []
    for n,i in enumerate(range(0, df.shape[0])):
        cosim = cosine_similarity([df.iloc[0],] , [df.iloc[i],])[0][0]
        sim_scores.append((n,cosim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 상위 4명, index 0은 client self
    sim_scores = sim_scores[0:4]
    idx = [i[0] for i in sim_scores]

    # print(sim_scores)
    # print(df.iloc[idx])

    # 유사한 유저 top 3
    sim_user = df.iloc[idx].index.to_list()[1:4]

    return sim_user


def movie_list_dict(q_movies, keep=None):
    if keep is None:
        movie_list=[]
        for movie in q_movies:
            movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
                                    "id":movie.naver_api_info.movie_id,
                                    "title_original":movie.naver_api_info.title_original,
                                    "image":movie.naver_api_info.image,
                                    "pubdate":movie.naver_api_info.pubdate,
                                    }
                                    )
        return movie_list

    if keep == 'rating':
        movie_list=[]
        for movie in q_movies:
            movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
                                    "id":movie.naver_api_info.movie_id,
                                    "rating":movie.client_rating
                                    }
                                    )
        return movie_list
                            
    if keep == 'keep':
        movie_list=[]
        for movie in q_movies:
            movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
                                "id":movie.naver_api_info.movie_id,
                                "title_original":movie.naver_api_info.title_original,
                                "image":movie.naver_api_info.image,
                                "pubdate":movie.naver_api_info.pubdate,
                                "youtube_url":youtube_api(movie.naver_api_info.title_original)
                                }
                                )
        return movie_list

    # if keep == 'rec':
    #     movie_list = []
    #     duplicats = []
    #     # 현재 랜더된 영화를 유지하면서 redirect
    #     for movie in get_render_movies(): 
    #         # print(movie, "=="*50)
    #         duplicats.append(movie.rendered_movies.movie_id)
    #         # print(duplicats, movie.rendered_movies.movie_id)
    #         if duplicats.count(movie.rendered_movies.movie_id) > 1:
    #             continue
    #         else :
    #             # print(movie, movie.naver_id,'++'*50)
    #             ## movie_list = "image", "title_kr", "pubdate", "title_original"
    #             movie_list.append({"title_kr":movie.naver_api_info.title_kr, 
    #                                 "id":movie.naver_api_info.movie_id,
    #                                 "title_original":movie.naver_api_info.title_original,
    #                                 "image":movie.naver_api_info.image,
    #                                 "pubdate":movie.naver_api_info.pubdate
    #                                 }
    #                                 )
    #     return movie_list