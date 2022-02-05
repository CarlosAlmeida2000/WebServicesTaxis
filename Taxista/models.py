from django.core.files.base import ContentFile
from django.db import models
from django.db import transaction
from django.db.models import F, Value, Q
from django.db.models.functions import Concat
from Usuario import models as md_usuario
from Servicio import models as md_servicio
from Cooperativa import models as md_cooperativa
from Usuario.File import File
import json, base64, os

file = File()
# Create your models here.
class Taxistas(models.Model):
    foto_cedula_f = models.ImageField(upload_to = 'Taxistas')
    foto_cedula_t = models.ImageField(upload_to = 'Taxistas')
    numero_placa = models.CharField(max_length = 8)
    foto_vehiculo = models.ImageField(upload_to = 'Taxistas')
    foto_matricula_f = models.ImageField(upload_to = 'Taxistas')
    foto_matricula_t = models.ImageField(upload_to = 'Taxistas')
    foto_licencia_f = models.ImageField(upload_to = 'Taxistas')
    foto_licencia_t = models.ImageField(upload_to = 'Taxistas')
    disponibilidad = models.CharField(max_length = 22)
    persona = models.OneToOneField(md_usuario.Personas, on_delete = models.PROTECT)

    @staticmethod
    def obtener_taxis(request):
        try:
            if 'id' in request.GET: 
                queryset_taxis = Taxistas.objects.filter(id = request.GET['id'])
            elif 'nom_taxista' in request.GET:
                queryset_taxis = (Taxistas.objects.all()).annotate(nombres_completos = Concat('persona__nombres', Value(' '), 'persona__apellidos'))
                queryset_taxis = queryset_taxis.filter(nombres_completos__icontains = request.GET['nom_taxista'])
            else:
                queryset_taxis = Taxistas.objects.all()
            taxistas = (queryset_taxis.select_related('persona').select_related('usuario')).annotate(eliminar = F('persona__usuario__habilitado')
            ).values('id', 'foto_cedula_f', 'foto_cedula_t', 'foto_vehiculo', 'foto_matricula_f', 'foto_matricula_t', 'foto_licencia_f', 'foto_licencia_t', 'numero_placa', 'disponibilidad',
            'persona_id', 'persona__nombres', 'persona__apellidos', 'persona__cedula', 'persona__telefono', 'persona__foto_perfil', 
            'persona__usuario_id', 'persona__usuario__correo', 'persona__usuario__habilitado', 'eliminar')
            for t in taxistas:
                if(t['foto_cedula_f'] != ''):
                    file.ruta = t['foto_cedula_f']
                    t['foto_cedula_f'] = file.get_base64()
                if(t['foto_cedula_t'] != ''):
                    file.ruta = t['foto_cedula_t']
                    t['foto_cedula_t'] = file.get_base64()
                if(t['foto_vehiculo'] != ''):
                    file.ruta = t['foto_vehiculo']
                    t['foto_vehiculo'] = file.get_base64()
                if(t['foto_matricula_f'] != ''):
                    file.ruta = t['foto_matricula_f']
                    t['foto_matricula_f'] = file.get_base64()
                if(t['foto_matricula_t'] != ''):
                    file.ruta = t['foto_matricula_t']
                    t['foto_matricula_t'] = file.get_base64()
                if(t['foto_licencia_f'] != ''):
                    file.ruta = t['foto_licencia_f']
                    t['foto_licencia_f'] = file.get_base64()
                if(t['foto_licencia_t'] != ''):
                    file.ruta = t['foto_licencia_t']
                    t['foto_licencia_t'] = file.get_base64()
                if(t['persona__foto_perfil'] != ''):
                    file.ruta = t['persona__foto_perfil']
                    t['persona__foto_perfil'] = file.get_base64()
                rol_usuario = md_usuario.RolesUsuario.objects.filter(usuario_id = t['persona__usuario_id']).select_related('rol')
                t['eliminar'] = False if(len(md_servicio.Servicios.objects.filter(taxista_id = t['id'])) > 0 or (len(rol_usuario.filter(rol__nombre = 'Taxista informal')) == 1 or len(md_cooperativa.CoopeTaxis.objects.filter(taxista_id = t['id'])) > 0)) else True
            return list(taxistas)
        except Taxistas.DoesNotExist:
            return 'No existe el taxista.'
        except Exception as e:
            return 'Sucedió un error al obtener los datos, por favor intente nuevamente.'

    def guardar_taxi(self, json_data, usuario, persona):
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
                    file.base64 = json_data['persona__foto_perfil']
                    file.nombre_file = 'usuario_' + str(usuario.id)
                    persona.foto_perfil = file.get_file()
                    if(ruta_img_borrar != ''):
                        os.remove(ruta_img_borrar)
                persona.usuario = usuario
                persona.save()
                if 'foto_cedula_f' in json_data:
                    file.base64 = json_data['foto_cedula_f']
                    file.nombre_file = 'foto_cedula_f_' + str(usuario.id)
                    self.foto_cedula_f = file.get_file()
                if 'foto_cedula_t' in json_data:
                    file.base64 = json_data['foto_cedula_t']
                    file.nombre_file = 'foto_cedula_t_' + str(usuario.id)
                    self.foto_cedula_t = file.get_file()
                if 'numero_placa' in json_data:
                    self.numero_placa = json_data['numero_placa']
                if 'foto_vehiculo' in json_data:
                    file.base64 = json_data['foto_vehiculo']
                    file.nombre_file = 'foto_vehiculo_' + str(usuario.id)
                    self.foto_vehiculo = file.get_file()
                if 'foto_matricula_f' in json_data:
                    file.base64 = json_data['foto_matricula_f']
                    file.nombre_file = 'foto_matricula_f_' + str(usuario.id)
                    self.foto_matricula_f = file.get_file()
                if 'foto_matricula_t' in json_data:
                    file.base64 = json_data['foto_matricula_t']
                    file.nombre_file = 'foto_matricula_t_' + str(usuario.id)
                    self.foto_matricula_t = file.get_file()
                if 'foto_licencia_f' in json_data:
                    file.base64 = json_data['foto_licencia_f']
                    file.nombre_file = 'foto_licencia_f_' + str(usuario.id)
                    self.foto_licencia_f = file.get_file()
                if 'foto_licencia_t' in json_data:
                    file.base64 = json_data['foto_licencia_t']
                    file.nombre_file = 'foto_licencia_t_' + str(usuario.id)
                    self.foto_licencia_t = file.get_file()
                if 'disponibilidad' in json_data:
                    self.disponibilidad = json_data['disponibilidad']
                self.persona = persona
                self.save()
                return True
        except Exception as e: 
            print(str(e))
            return False

    def eliminar_taxi(self):
        try:
            with transaction.atomic():
                persona = md_usuario.Personas.objects.get(id = self.persona.id)
                usuario = md_usuario.Usuarios.objects.get(id = persona.usuario.id)
                roles = md_usuario.RolesUsuario.objects.filter(usuario_id = usuario.id).select_related('rol').values('id', 'rol_id', 'rol__nombre')
                # Si tiene un único rol Taxista, se elimina por completo el usuario, persona y taxista
                if (len(roles) == 1 and (roles[0]['rol__nombre'] == 'Taxista formal' or roles[0]['rol__nombre'] == 'Taxista informal')):
                    rol_usuario = md_usuario.RolesUsuario.objects.get(id = roles[0]['id'])
                    rol_usuario.delete()
                    self.delete()
                    if(str(persona.foto_perfil) != ''):
                        os.remove(persona.foto_perfil.url[1:])
                    persona.delete()
                    usuario.delete()
                else:
                    # Se elimina sólo el rol de Taxista del usuario, porque tiene otros roles como: Cliente o Cooperativa o Administrador
                    rol_usuario = md_usuario.RolesUsuario.objects.get(id = roles.get(Q(rol__nombre = 'Taxista formal') | Q(rol__nombre = 'Taxista informal'))['id'])
                    rol_usuario.delete()
                    self.delete()
                return True
        except Exception as e: 
            return False
