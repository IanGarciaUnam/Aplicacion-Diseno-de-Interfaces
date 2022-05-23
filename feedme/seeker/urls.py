from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path('feedme', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register')
]