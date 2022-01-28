from django.db import models
from Usuario.models import Personas

# Create your models here.
class Taxistas(models.Model):
    foto_cedula_f = models.ImageField(upload_to = "Taxistas")
    foto_cedula_t = models.ImageField(upload_to = "Taxistas")
    numero_placa = models.CharField(max_length = 8)
    foto_vehiculo = models.ImageField(upload_to = "Taxistas")
    foto_matricula_f = models.ImageField(upload_to = "Taxistas")
    foto_matricula_t = models.ImageField(upload_to = "Taxistas")
    foto_licencia_f = models.ImageField(upload_to = "Taxistas")
    foto_licencia_t = models.ImageField(upload_to = "Taxistas")
    disponibilidad = models.CharField(max_length = 22)
    persona = models.ForeignKey(Personas, on_delete = models.PROTECT)
