from django.shortcuts import render
import requests
from django.db import connection
from playground.models import RegisterUser
from datetime import date


# Create your views here.
def home_page(request):
    return render(request, 'index.html')


def get_movies(request):
    api_key = "08a4cc722f0c09e91f63172cac468dc6"
    movie_data_list = []
    
    headers = {'Content-Type': 'application/json'}
    body = {
        "page": 1,
        "api_key": api_key,
        "language": "English"
    }
    get_movie_list_response = requests.get('https://api.themoviedb.org/4/list/1/', headers=headers, params=body)
    if get_movie_list_response.status_code == 200:
        for i in get_movie_list_response.json()['results']:
            response_url = 'https://image.tmdb.org/t/p/w500/{poster_url}'.format(poster_url=i['poster_path'])
            movie_data_list.append({
                'poster_path': response_url,
                'title': i['original_title'],
                'overview': i['overview']
            })
    else:
        raise ConnectionError

    return render(request, 'movies.html', {"movie_list": movie_data_list})


def sign_up_user(request):
    today_date = date.today()
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('password'):
            cursor = connection.cursor()
            query = 'INSERT INTO user (username, first_name, last_name, password, date_joined) ' \
                    'VALUES ("{username}", "{first_name}", "{last_name}", "{password}", STR_TO_DATE("{today_date}", "%Y-%m-%d"));' \
                .format(username=request.POST.get('username'), first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name'),
                        password=request.POST.get('password'), today_date=today_date)
            cursor.execute(query)
        else:
            return render(request, 'register.html', context={"warning": "Please fill the empty fields"})

        return render(request, 'index.html')
    else:
        return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            cursor = connection.cursor()
            query = 'SELECT * FROM user WHERE username="{username}" and password="{password}"'.format(username=request.POST.get('username'), password=request.POST.get('password'))
            cursor.execute(query)
            if cursor.fetchall():
                return render(request, 'index.html')

    return render(request, 'login.html')
