from django.db import models
from Usuario import models as md_usuario

# Create your models here.
class Clientes(models.Model):
    persona = models.OneToOneField('Usuario.Personas', on_delete = models.PROTECT)

class LugaresFavoritos(models.Model):
    nombre_sitio = models.CharField(max_length = 60)
    longitud = models.FloatField()
    latitud = models.FloatField()
    cliente = models.ForeignKey('Cliente.Clientes', on_delete = models.PROTECT, related_name = 'lugares')
