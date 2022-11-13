from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.conf import settings

from django.template import RequestContext

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


def get_coordinates():
    pass

def index(request):
    Lugar.objects.all().delete();
    r= Lugar(nombre="Facultad de Ciencias", direccion="Investigación Científica, C.U., Coyoacán, 04510 Ciudad de México, CDMX");
    r.save()
    tlahuizcalpan0=Edificio_Piso(nombre=r,nombre_edificio="Tlahuizcalpan", piso="Planta Baja", instrucciones_salida="Toma la salida más cercana \n Si te encuentras cerca al árbol central, repliegate a las paredes \n Mantente alejado de vidrios, ventanas u objetos que puedan caer o volcarse \n Manten la calma")
    tlahuizcalpan1=Edificio_Piso(nombre=r,nombre_edificio="Tlahuizcalpan", piso="1", instrucciones_salida="Toma la salida más cercana de tu lado izquierdo \n Dirigete al busto de Darwin (entrada principal) \n En la salida izquierda encontrarás el punto de reunión más cercano \n Espera instrucciones del personal de protección civil o personal capacitado \n Manten la calma")
    tlahuizcalpan2=Edificio_Piso(nombre=r,nombre_edificio="Tlahuizcalpan", piso="2", instrucciones_salida="Desciende al primer piso \n Dirigete al busto de Darwin (entrada principal) \n En la salida izquierda encontrarás el punto de reunión más cercano \n Espera instrucciones del personal de protección civil o personal capacitado \n Manten la calma")
    tlahuizcalpan3=Edificio_Piso(nombre=r,nombre_edificio="Tlahuizcalpan", piso="3",instrucciones_salida="Desciende al primer piso \n Dirigete al busto de Darwin (entrada principal) \n En la salida izquierda encontrarás el punto de reunión más cercano \n Espera instrucciones del personal de protección civil o personal capacitado \n Manten la calma")
    tlahuizcalpan0.save()
    tlahuizcalpan1.save()
    tlahuizcalpan2.save()
    tlahuizcalpan3.save()
    o_0=Edificio_Piso(nombre=r,nombre_edificio="Edificio O", piso="Planta Baja", instrucciones_salida="Dirigete a alguna de salidas con dirección al estacionamiento de profesores (a mano derecha de las escaleras si te encuentras por la entrada P cercana a la librería, izquierda en caso de encontrarte cerca de la papelería) \n ubica el punto de reunión más cercano en el estacionamiento \n Espera instrucciones del personal de protección civil ")
    o_0.save()
    o_1=Edificio_Piso(nombre=r,nombre_edificio="Edificio O", piso="1",instrucciones_salida="Toma las escaleras de salida más cercanas, si te encuentras en los números de salón 100 al 111, dirigete a tu mano derecha, en caso contrario a la izquierda \n En la planta baja, diregete a alguna de salidas con dirección al estacionamiento principal \n ubica el punto de reunión más cercano en el estacionamiento \n Espera instrucciones del personal de protección civil ")
    o_1.save()
    o_2=Edificio_Piso(nombre=r,nombre_edificio="Edificio O", piso="2", instrucciones_salida="Toma las escaleras de salida más cercanas, si te encuentras en los números de salón 200 al 211, dirigete a tu mano derecha, en caso contrario a la izquierda \n En la planta baja, diregete a alguna de salidas con dirección al estacionamiento principal \n ubica el punto de reunión más cercano en el estacionamiento \n Espera instrucciones del personal de protección civil ")
    o_2.save()
    p_0=Edificio_Piso(nombre=r,nombre_edificio="Edificio P", piso="Planta Baja", instrucciones_salida="Dirigete a alguna de salidas con dirección al estacionamiento de profesores (a mano derecha de las escaleras si te encuentras por la entrada P cercana a la librería, izquierda en caso de encontrarte cerca de la papelería) \n ubica el punto de reunión más cercano en el estacionamiento \n Espera instrucciones del personal de protección civil")
    p_0.save()
    p_1=Edificio_Piso(nombre=r,nombre_edificio="Edificio P", piso="1", instrucciones_salida="Toma las escaleras de salida más cercanas, si te encuentras en los números de salón 100 al 111, dirigete a tu mano derecha, en caso contrario a la izquierda \n En la planta baja, diregete a alguna de salidas con dirección al estacionamiento principal \n ubica el punto de reunión más cercano en el estacionamiento \n Espera instrucciones del personal de protección civil ")
    p_1.save()
    p_2=Edificio_Piso(nombre=r,nombre_edificio="Edificio P", piso="2",instrucciones_salida="Toma las escaleras de salida más cercanas, si te encuentras en los números de salón 200 al 211, dirigete a tu mano derecha, en caso contrario a la izquierda \n En la planta baja, diregete a alguna de salidas con dirección al estacionamiento principal \n ubica el punto de reunión más cercano en el estacionamiento \n Espera instrucciones del personal de protección civil ")
    p_2.save()
    encit= Lugar(nombre="(ENCIT) Escuela Nacional de Ciencias de la Tierra", direccion="Parque de los bigotes, C.U., Coyoacán, 04510 Ciudad de México, CDMX")
    encit.save()
    en_1=Edificio_Piso(nombre=encit, nombre_edificio="Principal", piso="Planta Baja", instrucciones_salida="Desciende las escaleras\n Dirigete a la zona de reunión  \n Espera instrucciones del personal de protección civil")
    en_2=Edificio_Piso(nombre=encit, nombre_edificio="Principal", piso="1", instrucciones_salida="Desciende las escaleras\n Dirigete a la zona de reunión en la planta baja \n Espera instrucciones del personal de protección civil")
    en_1.save()
    en_2.save()
    resultados=Lugar.objects.all();
    lugares= Edificio_Piso.objects.all()
    context={'resultados':resultados, "lugares":lugares}
    print(resultados)
    return render(request, 'seeker/index.html', context)


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


@csrf_exempt
def results_no_login(request):
    context = {}
    lugares=None
    instrucciones=""
    if request.method == 'GET' and request.GET.get('id') != None:
        id = request.GET.get('id')
        if len(str(id))>10:
            return  redirect('/')
        print(id)
        #Class.objects.get(pk=this_object_id)
        try:
            edificio_piso = Edificio_Piso.objects.get(pk=id)
            lugares=Edificio_Piso.objects.all()
            print(edificio_piso)
            print(edificio_piso.get_instrucciones_salida())
            instrucciones=edificio_piso.get_instrucciones_salida()
            context={'instrucciones':instrucciones,'lugar':edificio_piso ,'lugares':lugares, 'id_selected':id}
            #return render(request, 'seeker/404.html', context)
        except:
            return render(request, 'seeker/404.html')

        """
        resultados = None
        if tipo == 'alimento':
            key = request.GET.get('alimento')
            resultados = Alimento.objects.filter(nombre__icontains=key)
        else:
            key = request.GET.get('receta')
            resultados = Receta.objects.filter(nombre__icontains=key)

        context = {'resultados': resultados, 'tipo': tipo}

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'mostrar-alimento':
            idAlimento = request.POST.get('alimento')
            # Obtenemos el alimento.
            alimento = Alimento.objects.get(id=idAlimento)
            data = {
                'nombre': alimento.nombre,
                'calorias': alimento.calorias,
                'grasas': alimento.grasas,
                'proteina': alimento.proteina,
            }
            return JsonResponse({'data': data}, status=200)
            """
    return render(request, 'seeker/results.html', context)


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

def handler404(request, *args, **argv):
    response = render(request, 'seeker/404.html', {})
    response.status_code = 404
    return response
