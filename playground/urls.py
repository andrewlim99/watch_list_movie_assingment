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
    path('add_to_watch_list/', views.add_to_watch_list, name='add_to_watch_list'),
    path('watch_list/', views.watch_list_page),
    path('api/get_user_watch_list/', api.get_user_watch_list),
    path('api/delete_watch_list/<int:pk>', api.delete_watch_list),
    path('remove_watch_list/', views.remove_watch_list, name='remove_watch_list'),
    path('update_movie_notes/', views.update_movie_notes, name='update_movie_notes'),
    path('api/update_movie_notes/<int:pk>', api.update_movie_notes),
]