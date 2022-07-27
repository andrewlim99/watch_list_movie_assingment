from django.shortcuts import render
import requests
from django.db import connection
from datetime import date
from django.shortcuts import redirect
from playground.api import *


# Create your views here.
def get_logged_in_user(request):
    context = {"data": ""}
    if request.session.has_key("user"):
        context["data"] = request.session['user']

    return context


def home_page(request):
    context = get_logged_in_user(request)
    return render(request, 'index.html', context=context)


def get_movies(request):
    context = get_logged_in_user(request)
    if not context["data"]:
        return render(request, 'index.html', context=context)

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
                'movie_id': i['id'],
                'poster_path': response_url,
                'title': i['original_title'],
                'overview': i['overview']
            })
    else:
        raise ConnectionError
    context.update({"movie_list": movie_data_list})
    return render(request, 'movies.html', context=context)


def sign_up_user(request):
    today_date = date.today()
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('first_name') and request.POST.get(
                'last_name') and request.POST.get('password'):
            cursor = connection.cursor()
            query = 'INSERT INTO user (username, first_name, last_name, password, date_joined) ' \
                    'VALUES ("{username}", "{first_name}", "{last_name}", "{password}", STR_TO_DATE("{today_date}", "%Y-%m-%d"));' \
                .format(username=request.POST.get('username'), first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name'),
                        password=request.POST.get('password'), today_date=today_date)
            cursor.execute(query)
        else:
            return render(request, 'register.html', context={"warning": "Please fill the empty fields"})

        return redirect('../login/')
    else:
        return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            cursor = connection.cursor()
            query = 'SELECT * FROM user WHERE username="{username}" and password="{password}"'.format(
                username=request.POST.get('username'), password=request.POST.get('password'))
            cursor.execute(query)
            record = cursor.fetchone()
            if record:
                request.session["user"] = "{0}-{1}".format(record[0], record[1])
                return redirect('../home/')
            else:
                return render(request, 'login.html')

    return render(request, 'login.html')


def logout_user(request):
    request.session.flush()
    return redirect('../home/')


def add_to_watch_list(request):
    user_id = request.POST.get('user_data').split("-")[0]
    user_name = request.POST.get('user_data').split("-")[1]
    headers = {'Content-Type': 'application/json'}
    body = {
        "user_id": user_id,
        "movie_id": request.POST.get('movie_id'),
        "user_name": user_name,
        "movie_title": request.POST.get('movie_title'),
        "movie_url": str(request.POST.get('movie_poster_path'))
    }

    site_url = "http://{0}".format(request.get_host())
    get_movie_list_response = requests.post('{0}/api/add_watch_list'.format(site_url), headers=headers, json=body)
    if get_movie_list_response.status_code != 200:
        raise ConnectionError

    return redirect('../movies/')
