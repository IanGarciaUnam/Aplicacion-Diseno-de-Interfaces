from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path('feedme', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('reset-pass', views.reset_pass, name='reset-pass'),
    path('results-nl', views.results_no_login, name='results-nl')

    ]

