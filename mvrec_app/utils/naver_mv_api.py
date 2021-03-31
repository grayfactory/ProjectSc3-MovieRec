import requests
import re
from time import sleep

"""
movie_list 는 dictionary의 리스트
ex) {'title': 'Rocketeer, The (1991)', 'id': 2094}
"""
client_id = "e9M_YCsycX7H_JjeT9mL"
client_secret = "LwLTgtqvqf"

def naver_movie_api(movie_list):
    movie_list_kr = []

    for item in movie_list:
        # print(item)
        movie_dict = {}
        
        title_str = item['title']
        # print(re.findall('^.*?\(', title_str)[0][:-1])
        # print(re.findall('\(([^)]+)', title_str)[-1])
        title = re.findall('^.*?\(', title_str)[0][:-1]
        pubdate = re.findall('\(([^)]+)', title_str)[-1]
        
        movie=title
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        url = f"https://openapi.naver.com/v1/search/movie.json?query={movie}&display=100"
        res=requests.get(url,headers=header_parms)
        data =res.json()
        # print(data)
        if data['total'] > 1:
            
            for i in data['items']:
                if i['pubDate'] == pubdate:
                    
                    movie_dict['title_kr'] = i['title']
                    movie_dict['pubdate'] = i['pubDate']
                    movie_dict['image'] = i['image']
                    movie_dict['userRating'] = i['userRating']
                    movie_dict['actor'] = i['actor']
                    movie_dict['director'] = i['director']

                    break

                else :

                    movie_dict['title_kr'] = title
                    movie_dict['pubdate'] = pubdate
                    movie_dict['image'] = None
                    movie_dict['userRating'] = None
                    movie_dict['actor'] = None
                    movie_dict['director'] = None
                    
        elif data['total'] == 0:
            
            movie_dict['title_kr'] = title
            movie_dict['pubdate'] = pubdate
            movie_dict['image'] = None
            movie_dict['userRating'] = None
            movie_dict['actor'] = None
            movie_dict['director'] = None
            
        else :
            
            movie_dict['title_kr'] = data['items'][0]['title']
            movie_dict['pubdate'] = data['items'][0]['pubDate']
            movie_dict['image'] = data['items'][0]['image']
            movie_dict['userRating'] = data['items'][0]['userRating']
            movie_dict['actor'] = data['items'][0]['actor']
            movie_dict['director'] = data['items'][0]['director']
        movie_dict['title_original'] = title
        movie_dict['id']=item['id']
        movie_list_kr.append(movie_dict)

        sleep(0.05)

    return movie_list_kr

if __name__ == "__main__":
    # test 
    movie_list= [{'title': 'Rocketeer, The (1991)', 'id': 2094}, 
    {'title': 'Amazing Spider-Man, The (2012)', 'id': 95510}, 
    {'title': 'Kill Bill: Vol. 2 (2004)', 'id': 7438}, 
    {'title': 'Along Came a Spider (2001)', 'id': 4238}, 
    {'title': 'Rumble in the Bronx (Hont faan kui) (1995)', 'id': 112}, 
    {'title': 'In the Line of Fire (1993)', 'id': 474}, 
    {'title': 'Léon (1990)', 'id': 2616}]
    listed = naver_movie_api(movie_list)
    print(listed)
