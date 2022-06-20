from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateUserForm
import requests
from .decorators import usuario_no_autenticado, usuarios_permitidos


class HomeView(TemplateView):
    template_name = 'index.html'


def index(request):
    return render(request, 'seeker/index.html', {})


@usuario_no_autenticado
def loginPage(request):
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


@usuario_no_autenticado
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            tipoUsuario = 'tutor' if request.POST.get('tipo-usuario') != None else 'usuario'
            grupo = Group.objects.get(name=tipoUsuario)
            usuario.groups.add(grupo)
            if tipoUsuario == 'tutor':
                Tutor.objects.create(
                    user=usuario
                )
            else:
                Usuario.objects.create(
                    user=usuario
                )
                
            return redirect('login')

    context = {'form': form}

    return render(request, 'seeker/register.html', context)


def reset_pass(request):
    return render(request, 'seeker/reset-pass.html', {})


def results_no_login(request):
    # key=request.GET.get('buscar','')
    # print(key)
    #response = requests.get('https://api.edamam.com/api/nutrition-data?app_id=c933683d&app_key=5eae2dcc11aa5945fbf7d51d849af20d&nutrition-type=cooking&ingr='+'buscar')
    # Tranformamos la respuesta en un objeto JSON
    #todos = response.json()
    # print(todos)
    todos = {}
    return render(request, 'seeker/results-nl.html', {'results': todos})


def receta(request):
    return render(request, 'seeker/receta.html', {})


@login_required(login_url='login')
@usuarios_permitidos(roles_permitidos=['tutor'])
def esquema_tutor(request):
    if request.user.is_authenticated:
        # TODO: Validar que el usuario sea un tutor.
        # TODO: Si sí, obtenemos sus usuarios.
        usuarios = {}
        context = {'usuarios': usuarios}
        return render(request, 'seeker/esquema-tutor.html', context)
    else:
        return redirect('index')


@login_required(login_url='login')
@usuarios_permitidos(roles_permitidos=['usuario'])
def esquema_ul(request):
    return render(request, 'seeker/esquema-ul.html', {})
