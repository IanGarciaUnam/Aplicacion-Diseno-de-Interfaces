from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm


class HomeView(TemplateView):
    template_name = 'index.html'


def index_login(request):
    return render(request, 'seeker/index_login.html', {})

def index(request):
    return render(request, 'seeker/index.html', {})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index_login')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index_login')

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
    return render(request, 'seeker/results-nl.html', {})


def receta(request):
    return render(request, 'seeker/receta.html', {})
