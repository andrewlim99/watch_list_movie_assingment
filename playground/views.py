from django.shortcuts import render
import requests
from django.db import connection
from datetime import date
from django.shortcuts import redirect
from playground.api import *
from django.template import RequestContext


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
    add_to_watch_list_response = requests.post('{0}/api/add_watch_list'.format(site_url), headers=headers, json=body)
    if add_to_watch_list_response.status_code != 200:
        raise ConnectionError

    return redirect('../movies/')


def watch_list_page(request):
    user_id = request.session['user']
    login_user = get_logged_in_user(request)
    user_id = user_id.split("-")[0]
    context = {
        "movie_list": []
    }
    headers = {'Content-Type': 'application/json'}
    body = {
        "user_id": user_id
    }

    site_url = "http://{0}".format(request.get_host())
    get_user_watch_list_response = requests.get('{0}/api/get_user_watch_list'.format(site_url), headers=headers, params=body)
    if get_user_watch_list_response.status_code == 200:
        for item in get_user_watch_list_response.json():
            context['movie_list'].append({
                "id": item['id'],
                "user_id": item['user_id'],
                "user_name": item['user_name'],
                "movie_id": item['movie_id'],
                "movie_title": item['movie_title'],
                "movie_notes": item['movie_notes'],
                "movie_url": item['movie_url']
            })
    context.update(login_user)
    return render(request, 'watch_list.html', context=context)


def remove_watch_list(request):
    headers = {'Content-Type': 'application/json'}
    deleted_id = request.POST.get('watch_list_id')
    site_url = "http://{0}".format(request.get_host())
    get_user_watch_list_response = requests.delete('{0}/api/delete_watch_list/{1}'.format(site_url, deleted_id), headers=headers)
    if get_user_watch_list_response.status_code != 200:
        raise ConnectionError

    return redirect('../watch_list/')


def update_movie_notes(request):
    headers = {'Content-Type': 'application/json'}
    updated_id = request.POST.get('id')
    site_url = "http://{0}".format(request.get_host())
    json = {
        "movie_notes": request.POST.get('movie_notes')
    }
    get_user_watch_list_response = requests.put('{0}/api/update_movie_notes/{1}'.format(site_url, updated_id),
                                                   headers=headers, json=json)
    context = {'movie_id': request.POST.get('id')}
    if get_user_watch_list_response.status_code == 200:
        context.update({'response': 'Success'})

    return render(request, 'update_movie_notes.html', context=context)
