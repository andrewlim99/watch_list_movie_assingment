from django.urls import path, include
from . import views
from . import api

urlpatterns = [
    path('home/', views.home_page),
    path('movies/', views.get_movies),
    path('register/', views.sign_up_user),
    path('login/', views.login_user),
    path('signout/', views.logout_user),
    path('api/add_watch_list', api.insert_movie_to_user_watch_list),
    path('add_to_watch_list/', views.add_to_watch_list, name='add_to_watch_list')
]