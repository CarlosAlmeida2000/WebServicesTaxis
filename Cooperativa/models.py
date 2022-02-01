from django.core.files.base import ContentFile
from django.db import models
from django.db import transaction
from Taxista.models import *
from Usuario.models import *
import json, base64, os

# Create your models here.
class Cooperativas(models.Model):
    nom_cooperativa = models.CharField(max_length = 40)
    telefono = models.CharField(max_length = 10)
    direccion = models.TextField()
    ingresar_cobro = models.BooleanField(default = True)
    persona = models.OneToOneField(Personas, on_delete = models.PROTECT)

    def guardar_coop(self, json_data, usuario, persona):
        try:
            with transaction.atomic():
                usuario.correo = json_data['usuario']
                usuario.clave = json_data['clave']
                usuario.save()
                if 'rol' in json_data:
                    roles = RolesUsuario()
                    roles.usuario = usuario
                    roles.rol = (Roles.objects.get(nombre = json_data['rol']))
                    roles.save()
                persona.nombres = json_data['nombres_gerente']
                persona.apellidos = json_data['apellidos_gerente']
                persona.cedula = json_data['cedula_gerente']
                persona.telefono = json_data['telefono_gerente']
                if 'foto_perfil' in json_data:
                    ruta_img_borrar = ""
                    if(str(persona.foto_perfil) != ''):
                        ruta_img_borrar = persona.foto_perfil.url
                    image_b64 = json_data['foto_perfil']
                    format, img_body = image_b64.split(';base64,')
                    extension = format.split('/')[-1]
                    img_file = ContentFile(base64.b64decode(img_body), name = 'usuario_' + str(usuario.id) + '.' + extension)
                    persona.foto_perfil = img_file
                    if(ruta_img_borrar != ''):
                        os.remove(ruta_img_borrar)
                persona.usuario = usuario
                persona.save()
                self.nom_cooperativa = json_data['nom_cooperativa']
                self.telefono = json_data['telefono_coop']
                self.direccion = json_data['direccion_coop']
                self.persona = persona
                self.save()
                return True
        except Exception as e: 
            print("error ", str(e))
            return False

class CoopeTaxis(models.Model):
    cooperativa = models.ForeignKey(Cooperativas, on_delete = models.PROTECT, related_name = 'cooperativas')
    taxista = models.OneToOneField(Taxistas, on_delete = models.PROTECT, related_name = 'taxista')
