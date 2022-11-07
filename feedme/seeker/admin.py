from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Lugar)
admin.site.register(Alimento)
admin.site.register(Receta)
admin.site.register(Ingrediente)
admin.site.register(Usuario)
admin.site.register(Tutor)
