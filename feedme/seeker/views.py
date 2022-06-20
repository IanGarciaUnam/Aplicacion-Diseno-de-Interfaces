from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

# Create your views here.
from .models import *
from .forms import CreateUserForm
import requests
from .decorators import usuario_no_autenticado, usuarios_permitidos
from django.views.decorators.csrf import csrf_exempt, csrf_protect


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
            tipoUsuario = 'tutor' if request.POST.get(
                'tipo-usuario') != None else 'usuario'
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
    # response = requests.get('https://api.edamam.com/api/nutrition-data?app_id=c933683d&app_key=5eae2dcc11aa5945fbf7d51d849af20d&nutrition-type=cooking&ingr='+'buscar')
    # Tranformamos la respuesta en un objeto JSON
    # todos = response.json()
    # print(todos)
    todos = {}
    return render(request, 'seeker/results-nl.html', {'results': todos})


def receta(request):
    titulo = 'No has especificado ninguna receta'
    hayReceta = False
    receta = None
    calorias = 0
    if request.method == 'GET' and request.GET.get('nombre') != None:
        hayReceta = True
        titulo = request.GET.get('nombre').replace('-', ' ')
        # Obtenemos la receta.
        receta = Receta.objects.get(nombre=titulo)
        # Calculamos las calorías de acuerdo a las calorías de los almentos que contiene.
        calorias = 0
        for alimento in receta.alimento.all():
            calorias += alimento.calorias

    context = {'titulo': titulo, 'hayReceta': hayReceta, 'receta': receta, 'calorias': calorias}
    return render(request, 'seeker/receta.html', context)


@csrf_exempt
@login_required(login_url='login')
@usuarios_permitidos(roles_permitidos=['tutor', 'usuario'])
def esquema(request):
    grupo = request.user.groups.all()[0].name
    context = {'grupo': grupo}
    if grupo == 'tutor':
        if request.method == 'POST':
            accion = request.POST.get('accion')

            if accion == 'mostrar-usuarios':
                usuario = request.POST.get('usuario')
                # Obtenemos los clientes del usuario.
                clientesUsuario = Tutor.objects.get(
                    user_id=usuario).usuarios.all()
                # Obtenemos las usuarios que no son sus clientes.
                usuarios = Usuario.objects.exclude(id__in=clientesUsuario)
                # Guardamos la información que regresaremos.
                data = {}
                c = 0
                for usr in usuarios:
                    data.update(
                        {c: {'nombre': usr.user.username, 'id': usr.id}})
                    c += 1
                return JsonResponse({'data': data}, status=200)

            if accion == 'agregar-cliente':
                idCliente = request.POST.get('cliente')
                idUsuario = request.POST.get('usuario')
                # Obtenemos al usuario de la bd y al cliente que le agregaremos.
                usuario = Tutor.objects.get(user_id=idUsuario)
                u = Usuario.objects.get(id=idCliente)
                # Agregamos al cliente.
                usuario.usuarios.add(u)
                # Obtenemos las recetas del nuevo cliente para poder atualizar el acordeón de clientes.
                recetasUsuario = Usuario.objects.get(
                    id=idCliente).recetas.all()
                data = {}
                c = 0
                for receta in recetasUsuario:
                    data.update(
                        {c: {'nombre': receta.nombre, 'id': receta.id}})
                    c += 1
                return JsonResponse({'data': data}, status=200)

            if accion == 'mostrar-recetas':
                usuario = request.POST.get('usuario')
                # Obtenemos al usuario de la bd.
                id = User.objects.get(username=usuario).id
                # Obtenemos sus recetas
                recetasUsuario = Usuario.objects.get(user_id=id).recetas.all()
                # Obtenemos las recetas que le faltan.
                recetas = Receta.objects.exclude(id__in=recetasUsuario)
                # Guardamos la información que regresaremos.
                data = {}
                c = 0
                for receta in recetas:
                    data.update(
                        {c: {'nombre': receta.nombre, 'id': receta.id}})
                    c += 1
                return JsonResponse({'data': data}, status=200)

            if accion == 'agregar-receta':
                usuario = request.POST.get('usuario')
                receta = request.POST.get('receta')
                # Obtenemos al usuario de la bd y la receta que le agregaremos.
                idUsuario = User.objects.get(username=usuario).id
                usuario = Usuario.objects.get(user_id=idUsuario)
                r = Receta.objects.get(id=receta)
                # Agregamos la receta.
                usuario.recetas.add(r)
                return JsonResponse({}, status=200)

            if accion == 'eliminar-receta':
                idUsuario = request.POST.get('usuario')
                receta = request.POST.get('receta')
                # Obtenemos al usuario de la bd y la receta que le quitaremos.
                usuario = Usuario.objects.get(id=idUsuario)
                r = Receta.objects.get(id=receta)
                # Eliminamos la receta.
                usuario.recetas.remove(r)
                return JsonResponse({}, status=200)

        usuarios = Tutor.objects.get(user_id=request.user.id).usuarios.all()
        context.update({'usuarios': usuarios})

    else:
        # Obtenemos las recetas del usuario para mostrarlas en el template.
        recetas = Usuario.objects.get(user_id=request.user.id).recetas.all()
        context.update({'recetas': recetas})

    return render(request, 'seeker/esquema.html', context)
