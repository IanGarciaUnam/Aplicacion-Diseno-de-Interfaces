from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('results-nl', views.results_no_login, name='/?buscar={{x}}'),
=======
    path('results-nl', views.buscar, name='/?buscar='),
>>>>>>> main
    path('register', views.register, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('reset-pass', views.reset_pass, name='reset-pass'),
    path('results-nl', views.results_no_login, name='results-nl'),
    path('receta', views.receta, name='receta'),
    path('esquema', views.esquema, name='esquema'),
]
