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

    @staticmethod
    def obtener_coop(request):
        try:
            if 'nom_cooperativa' in request.GET:
                queryset_coop = Cooperativas.objects.filter(nom_cooperativa__icontains = request.GET['nom_cooperativa'])
            else:
                queryset_coop = Cooperativas.objects.all()
            cooperativas = (queryset_coop.select_related('persona').select_related('usuario')
            ).values('id', 'nom_cooperativa', 'telefono', 'direccion', 'ingresar_cobro', 
            'persona_id', 'persona__nombres', 'persona__apellidos', 'persona__cedula', 'persona__telefono', 'persona__foto_perfil', 
            'persona__usuario_id', 'persona__usuario__correo')
            for c in cooperativas:
                if(c['persona__foto_perfil'] != ''):
                    encoded_string = 'data:image/PNG;base64,' + str(base64.b64encode(open(str('media/' + c['persona__foto_perfil']), 'rb').read()))[2:][:-1]
                    c['persona__foto_perfil'] = encoded_string
            return list(cooperativas)
        except Cooperativas.DoesNotExist:
            return 'No existe la cooperativa.'
        except Exception as e:
            return 'Sucedió un error al obtener los datos, por favor intente nuevamente.'

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
                if 'foto_perfil' in json_data and str(json_data['foto_perfil']) != '':
                    ruta_img_borrar = ''
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
            return False

class CoopeTaxis(models.Model):
    cooperativa = models.ForeignKey(Cooperativas, on_delete = models.PROTECT, related_name = 'cooperativas')
    taxista = models.OneToOneField(Taxistas, on_delete = models.PROTECT, related_name = 'taxista')
