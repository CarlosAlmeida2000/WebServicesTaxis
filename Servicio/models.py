from django.db import models
from Taxista import models as md_taxista
from Cliente import models as md_cliente

# Create your models here.
class Servicios(models.Model):
    longitud_cliente = models.FloatField()
    latitud_cliente = models.FloatField()
    longitud_destino = models.FloatField()
    latitud_destino = models.FloatField()
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(null = True, blank = True)
    aceptada_tx = models.BooleanField(default = False)
    rechazada = models.BooleanField(default = False)
    culminada_tx = models.BooleanField(default = False)
    valor_cobrado = models.DecimalField(max_digits = 6, decimal_places = 2, null = True, blank = True)
    taxista = models.ForeignKey('Taxista.Taxistas', on_delete = models.PROTECT, related_name = 'taxistas')
    cliente = models.ForeignKey('Cliente.Clientes', on_delete = models.PROTECT, related_name = 'clientes')