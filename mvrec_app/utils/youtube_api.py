import requests


def youtube_api(title_original):

    key = 'AIzaSyA0CFMxTI0saf2w3JFKYboT2kcaaMb1VB0'
    query = title_original + ' trailer'
    maxvalue=1
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&key={key}&q={query}&maxResults={maxvalue}'
    res=requests.get(url)

    data = res.json()
    vid = data['items'][0]['id']['videoId']

    return f'https://www.youtube.com/watch?v={vid}'