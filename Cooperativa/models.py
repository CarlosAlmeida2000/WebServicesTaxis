from django.db import models
from Taxista.models import Taxistas
from Usuario.models import Personas

# Create your models here.
class Cooperativas(models.Model):
    nom_cooperativa = models.CharField(max_length = 40)
    telefono = models.CharField(max_length = 10)
    direccion = models.TextField()
    ingresar_cobro = models.BooleanField(default = True)
    persona = models.ForeignKey(Personas, on_delete = models.PROTECT)

class CoopeTaxis(models.Model):
    cooperativa = models.ForeignKey(Cooperativas, on_delete = models.PROTECT, related_name = "cooperativas")
    taxista = models.ForeignKey(Taxistas, on_delete = models.PROTECT, related_name = "taxista")
