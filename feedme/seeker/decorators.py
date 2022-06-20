from django.http import HttpResponse
from django.shortcuts import redirect


def usuario_no_autenticado(func_view):
    def func_envolvente(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return func_view(request, *args, **kwargs)
    return func_envolvente


def usuarios_permitidos(roles_permitidos=[]):
    def decorator(func_view):
        def func_envolvente(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in roles_permitidos:
                return func_view(request, *args, **kwargs)
            else:
                return HttpResponse('No tienes permiso para entrar a esta página.')
        return func_envolvente
    return decorator
