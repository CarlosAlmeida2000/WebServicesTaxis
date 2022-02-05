from django.core.files.base import ContentFile
from django.db import models
from django.db import transaction
from django.db.models import F
from Usuario import models as md_usuario
from Taxista import models as md_taxista
from Usuario.File import File
import json, base64, os

file = File()
# Create your models here.
class Cooperativas(models.Model):
    nom_cooperativa = models.CharField(max_length = 40)
    telefono = models.CharField(max_length = 10)
    direccion = models.TextField()
    ingresar_cobro = models.BooleanField(default = True)
    persona = models.OneToOneField('Usuario.Personas', on_delete = models.PROTECT)

    @staticmethod
    def obtener_coop(request):
        try:
            if 'id' in request.GET: 
                queryset_coop = Cooperativas.objects.filter(id = request.GET['id'])
            elif 'nom_cooperativa' in request.GET:
                queryset_coop = Cooperativas.objects.filter(nom_cooperativa__icontains = request.GET['nom_cooperativa'])
            else:
                queryset_coop = Cooperativas.objects.all()
            cooperativas = (queryset_coop.select_related('persona').select_related('usuario')).annotate(eliminar = F('persona__usuario__habilitado')
            ).values('id', 'nom_cooperativa', 'telefono', 'direccion', 'ingresar_cobro', 
            'persona_id', 'persona__nombres', 'persona__apellidos', 'persona__cedula', 'persona__telefono', 'persona__foto_perfil', 
            'persona__usuario_id', 'persona__usuario__correo', 'persona__usuario__habilitado', 'eliminar')
            for c in cooperativas:
                if(c['persona__foto_perfil'] != ''):
                    file.ruta = c['persona__foto_perfil']
                    c['persona__foto_perfil'] = file.get_base64()
                c['eliminar'] = False if len(CoopeTaxis.objects.filter(cooperativa_id = c['id'])) > 0 else True
            return list(cooperativas)
        except Cooperativas.DoesNotExist:
            return 'No existe la cooperativa.'
        except Exception as e:
            return 'Sucedió un error al obtener los datos, por favor intente nuevamente.'

    def guardar_coop(self, json_data, usuario, persona):
        try:
            with transaction.atomic():
                # atrapar la excepción de usuario repetido, unique
                # tambien validar si la persona ya se encuentra registrada, se agrega el nuevo rol y demas datos
                if 'persona__usuario__correo' in json_data:
                    usuario.correo = json_data['persona__usuario__correo']
                if 'persona__usuario__clave' in json_data:
                    usuario.clave = json_data['persona__usuario__clave']
                if 'persona__usuario__habilitado' in json_data:
                    usuario.habilitado = json_data['persona__usuario__habilitado']
                usuario.save()
                if 'usuario__rol' in json_data:
                    roles = md_usuario.RolesUsuario()
                    roles.usuario = usuario
                    roles.rol = (md_usuario.Roles.objects.get(nombre = json_data['usuario__rol']))
                    roles.save()
                if 'persona__nombres' in json_data:
                    persona.nombres = json_data['persona__nombres']
                if 'persona__apellidos' in json_data:
                    persona.apellidos = json_data['persona__apellidos']
                if 'persona__cedula' in json_data:
                    persona.cedula = json_data['persona__cedula']
                if 'persona__telefono' in json_data:
                    persona.telefono = json_data['persona__telefono']
                if 'persona__foto_perfil' in json_data and json_data['persona__foto_perfil'] != '':
                    ruta_img_borrar = ''
                    if(str(persona.foto_perfil) != ''):
                        ruta_img_borrar = persona.foto_perfil.url[1:]
                    file = File()
                    file.base64 = json_data['persona__foto_perfil']
                    file.nombre_file = 'usuario_' + str(usuario.id)
                    persona.foto_perfil = file.get_file()
                    if(ruta_img_borrar != ''):
                        os.remove(ruta_img_borrar)
                persona.usuario = usuario
                persona.save()
                if 'nom_cooperativa' in json_data:
                    self.nom_cooperativa = json_data['nom_cooperativa']
                if 'telefono' in json_data:
                    self.telefono = json_data['telefono']
                if 'direccion' in json_data:
                    self.direccion = json_data['direccion']
                if 'ingresar_cobro' in json_data:
                    self.ingresar_cobro = json_data['ingresar_cobro']
                self.persona = persona
                self.save()
                return True
        except Exception as e: 
            print(str(e))
            return False

    def eliminar_coop(self):
        try:
            with transaction.atomic():
                persona = md_usuario.Personas.objects.get(id = self.persona.id)
                usuario = md_usuario.Usuarios.objects.get(id = persona.usuario.id)
                roles = md_usuario.RolesUsuario.objects.filter(usuario_id = usuario.id).select_related('rol').values('id', 'rol_id', 'rol__nombre')
                # Si tiene un único rol Cooperativa, se elimina por completo el usuario, persona y cooperativa
                if (len(roles) == 1 and roles[0]['rol__nombre'] == 'Cooperativa'):
                    rol_usuario = md_usuario.RolesUsuario.objects.get(id = roles[0]['id'])
                    rol_usuario.delete()
                    self.delete()
                    if(str(persona.foto_perfil) != ''):
                        os.remove(persona.foto_perfil.url[1:])
                    persona.delete()
                    usuario.delete()
                else:
                    # Se elimina sólo el rol de Cooperativa del usuario, porque tiene otros roles como: Cliente o Taxista o Administrador
                    rol_usuario = md_usuario.RolesUsuario.objects.get(id = roles.get(rol__nombre = 'Cooperativa')['id'])
                    rol_usuario.delete()
                    self.delete()
                return True
        except Exception as e: 
            return False

class CoopeTaxis(models.Model):
    cooperativa = models.ForeignKey('Cooperativa.Cooperativas', on_delete = models.PROTECT, related_name = 'cooperativas')
    taxista = models.OneToOneField('Taxista.Taxistas', on_delete = models.PROTECT, related_name = 'taxista')
