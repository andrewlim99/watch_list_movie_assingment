from django.shortcuts import render
import requests


# Create your views here.
def home_page(request):
    return render(request, 'index.html')


def get_movie(request):
    api_key = "08a4cc722f0c09e91f63172cac468dc6"
    movie_data_list = []
    
    headers = {'Content-Type': 'application/json'}
    body = {
        "page": 1,
        "api_key": api_key,
        "language": "English"
    }
    get_movie_list_response = requests.get('https://api.themoviedb.org/4/list/1/', headers=headers, params=body).json()
    for i in get_movie_list_response['results']:
        response_url = 'https://image.tmdb.org/t/p/w500/{poster_url}'.format(poster_url=i['poster_path'])
        movie_data_list.append({
            'poster_path': response_url,
            'title': i['original_title'],
            'overview': i['overview']
        })
    print(movie_data_list)
    return render(request, 'index.html', {"movie_list": movie_data_list})
