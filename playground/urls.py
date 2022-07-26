from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_page),
    path('movies/', views.get_movies),
    path('register/', views.sign_up_user),
    path('login/', views.login_user)
]