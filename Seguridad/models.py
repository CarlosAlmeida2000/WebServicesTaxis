from django.db import models

# Create your models here.
class ContactosEmergencia(models.Model):
    persona = models.ForeignKey('Usuario.Personas', on_delete = models.PROTECT, related_name = 'amigos')
    persona_amigo = models.ForeignKey('Usuario.Personas', on_delete = models.PROTECT)
    es_amigo = models.BooleanField(default = False)

class Emergencias(models.Model):
    longitud_actual = models.FloatField()
    latitud_actual = models.FloatField()
    fecha_hora_alerta = models.DateTimeField()
    ultima_fecha_hora = models.DateTimeField()
    persona = models.ForeignKey('Usuario.Personas', on_delete = models.PROTECT, related_name = 'emergencias')
    servicio = models.OneToOneField('Servicio.Servicios', on_delete = models.PROTECT, null = True, blank = True)

