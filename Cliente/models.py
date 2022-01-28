from django.db import models
from Usuario.models import Personas

# Create your models here.
class Clientes(models.Model):
    persona = models.ForeignKey(Personas, on_delete = models.PROTECT)

class LugaresFavoritos(models.Model):
    nombre_sitio = models.CharField(max_length = 60)
    longitud = models.FloatField()
    latitud = models.FloatField()
    cliente = models.ForeignKey(Clientes, on_delete = models.PROTECT, related_name = "lugares")
