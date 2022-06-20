from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Alimento(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    calorias = models.FloatField(null=True)
    grasas = models.FloatField(null=True)
    proteina = models.FloatField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    alimento = models.ManyToManyField(Alimento)
    nombre = models.CharField(max_length=200, null=True)
    #calorias = models.FloatField(null=True)
    preparacion = models.TextField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def calorias_totales(self):
        suma_kcal=0
        for al in self.alimento.all():
            suma_kcal+=al.calorias
        return suma_kcal
    """
    def save(self, *args, **kwargs):
          self.calorias = self.get_calorias()
          super(Receta, self).save(*args, **kwargs)
    """
    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    receta = models.ManyToManyField(Receta)
    alimento = models.ManyToManyField(Alimento)
    porcion = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.alimento)+self.porcion



class Usuario(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    recetas = models.ManyToManyField(Receta)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __user__(self):
        return self.user


class Tutor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(Usuario)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __user__(self):
        return self.user
