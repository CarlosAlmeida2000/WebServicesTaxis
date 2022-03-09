from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from Usuario import models as md_usuario
from Usuario.File import File

file = File()
# Create your models here.
class Clientes(models.Model):
    persona = models.OneToOneField('Usuario.Personas', on_delete = models.PROTECT)

    @staticmethod
    def obtener_clientes(request):
        try:
            if 'id' in request.GET: 
                queryset_clientes = Clientes.objects.filter(id = request.GET['id'])
            elif 'nom_cliente' in request.GET:
                queryset_clientes = (Clientes.objects.all().select_related('persona')).annotate(nombres_completos = Concat('persona__nombres', Value(' '), 'persona__apellidos'))
                queryset_clientes = queryset_clientes.filter(nombres_completos__icontains = request.GET['nom_cliente'])
            else:
                queryset_clientes = Clientes.objects.all()
                print(len(queryset_clientes))
            # obtener todos los datos de las relaciones
            clientes = (queryset_clientes.select_related('persona').select_related('usuario')
            ).values('id', 'persona_id', 'persona__nombres', 'persona__apellidos', 'persona__cedula', 'persona__telefono', 'persona__foto_perfil', 
            'persona__usuario_id', 'persona__usuario__correo', 'persona__usuario__habilitado')
            # ciclo para determinar los cooperativas que se pueden eliminar y convertir la imagen a base64
            for c in clientes:
                if(c['persona__foto_perfil'] != ''):
                    file.ruta = c['persona__foto_perfil']
                    c['persona__foto_perfil'] = file.get_base64()
            return list(clientes)
        except Clientes.DoesNotExist:
            return 'No existe el cliente'
        except Exception as e:
            return 'error'

    def guardar_cliente(self, json_data):
        try:
            respuesta, usuario = self.persona.usuario.guardar_usuario(json_data, 'Cliente')
            if respuesta == 'correo repetido':
                return respuesta
            if respuesta == 'otro rol':
                self.persona = md_usuario.Personas.objects.get(usuario_id = usuario.id)
            self.persona.usuario = usuario
            respuesta, persona = self.persona.guardar_persona(json_data)
            if len(md_usuario.RolesUsuario.objects.filter(usuario_id = usuario.id).select_related('rol').filter(rol__nombre = 'Cliente')) == 0:
                roles = md_usuario.RolesUsuario()
                roles.usuario = usuario
                roles.rol = (md_usuario.Roles.objects.get(nombre = 'Cliente'))
                roles.save()
            self.persona = persona
            self.save()
            return 'guardado'
        except Exception as e: 
            return 'error' 

class LugaresFavoritos(models.Model):
    nombre_sitio = models.CharField(max_length = 60)
    longitud = models.FloatField()
    latitud = models.FloatField()
    cliente = models.ForeignKey('Cliente.Clientes', on_delete = models.PROTECT, related_name = 'lugares')
