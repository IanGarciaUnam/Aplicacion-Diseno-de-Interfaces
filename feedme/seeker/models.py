from django.db import models

# Create your models here.


class Alimento(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    calorias = models.FloatField(null=True)


class Receta(models.Model):
    alimento = models.ManyToManyField(Alimento)
    nombre = models.CharField(max_length=200, null=True)
    calorias = models.FloatField(null=True)
