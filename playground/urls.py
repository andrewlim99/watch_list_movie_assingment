from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_page),
    path('test/', views.get_movie),
]