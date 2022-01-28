from django.db import models
from WebServicesTaxis.Usuario.models import Personas

# Create your models here.
class ContactosEmergencia(models.Model):
    persona = models.ForeignKey(Personas, on_delete = models.PROTECT, related_name = "personas")
    persona_amigo = models.ForeignKey(Personas, on_delete = models.PROTECT, related_name = "personas_amigos")
    es_amigo = models.BooleanField(default = False)

class Emergencias(models.Model):
    longitud_actual = models.FloatField()
    latitud_actual = models.FloatField()
    fecha_hora_alerta = models.DateTimeField()
    ultima_fecha_hora = models.DateTimeField()
    persona = models.ForeignKey(Personas, on_delete = models.PROTECT, related_name = "personas")
    servicio = models.ForeignKey(Personas, on_delete = models.PROTECT, related_name = "servicios", null = True, blank = True)

