from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm
import requests


class HomeView(TemplateView):
    template_name = 'index.html'


def index(request):
    return render(request, 'seeker/index.html', {})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

        context = {}
        return render(request, 'seeker/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        context = {'form': form}

        return render(request, 'seeker/register.html', context)


def reset_pass(request):
    return render(request, 'seeker/reset-pass.html', {})


def results_no_login(request):
    #key=request.GET.get('buscar','')
    #print(key)
    #response = requests.get('https://api.edamam.com/api/nutrition-data?app_id=c933683d&app_key=5eae2dcc11aa5945fbf7d51d849af20d&nutrition-type=cooking&ingr='+'buscar')
    # Tranformamos la respuesta en un objeto JSON
    #todos = response.json()
    #print(todos)
    return render(request, 'seeker/results-nl.html', {'results':todos})


def receta(request):
    return render(request, 'seeker/receta.html', {})

def esquema_tutor(request):
    return render(request, 'seeker/esquema-tutor.html', {})

def esquema_ul(request):
    return render(request, 'seeker/esquema-ul.html', {})
