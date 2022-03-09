from django.db import models
from django.db import transaction
from django.db.models import F, Value, Q
from django.db.models.functions import Concat
from Usuario import models as md_usuario
from Servicio import models as md_servicio
from Cooperativa import models as md_cooperativa
from Usuario.File import File
import os

ls_campos = ['foto_cedula_f', 'foto_cedula_t', 'foto_vehiculo', 'foto_matricula_f', 'foto_matricula_t', 'foto_licencia_f', 'foto_licencia_t', 'persona__foto_perfil']
file = File()
# Create your models here.
class Taxistas(models.Model):
    foto_cedula_f = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    foto_cedula_t = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    numero_placa = models.CharField(max_length = 8)
    foto_vehiculo = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    foto_matricula_f = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    foto_matricula_t = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    foto_licencia_f = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    foto_licencia_t = models.ImageField(upload_to = 'Taxistas', null = True, blank = True)
    disponibilidad = models.CharField(max_length = 22)
    persona = models.OneToOneField(md_usuario.Personas, on_delete = models.PROTECT)
    
    @staticmethod
    def obtener_taxis(request):
        try:
            # Listar los taxis de una cooperativa
            if 'id_cooperativa' in request.GET:
                taxis = md_cooperativa.CoopeTaxis.objects.filter(cooperativa__id = request.GET['id_cooperativa'])
                queryset_taxis = Taxistas.objects.all().exclude(~Q(pk__in = taxis.prefetch_related('taxista').values('taxista_id')))
            elif 'id' in request.GET: 
                queryset_taxis = Taxistas.objects.filter(id = request.GET['id'])
            elif 'nom_taxista' in request.GET:
                queryset_taxis = (Taxistas.objects.all().select_related('persona')).annotate(nombres_completos = Concat('persona__nombres', Value(' '), 'persona__apellidos'))
                queryset_taxis = queryset_taxis.filter(nombres_completos__icontains = request.GET['nom_taxista'])
            else:
                queryset_taxis = Taxistas.objects.all()
            # obtener todos los datos de las relaciones
            taxistas = (queryset_taxis.select_related('persona').select_related('usuario')).annotate(eliminar = F('persona__usuario__habilitado')
            ).values('id', 'foto_cedula_f', 'foto_cedula_t', 'foto_vehiculo', 'foto_matricula_f', 'foto_matricula_t', 'foto_licencia_f', 'foto_licencia_t', 'numero_placa', 'disponibilidad',
            'persona_id','persona__nombres', 'persona__apellidos', 'persona__cedula', 'persona__telefono', 'persona__foto_perfil', 
            'persona__usuario_id', 'persona__usuario__correo', 'persona__usuario__habilitado', 'eliminar')
            # ciclo para determinar los taxistas que se pueden eliminar y convertir las imágenes a base64
            for t in taxistas:
                for campo in ls_campos:
                    if(t[campo] != ''):
                        file.ruta = t[campo]
                        t[campo] = file.get_base64()
                rol_usuario = md_usuario.RolesUsuario.objects.filter(usuario_id = t['persona__usuario_id']).select_related('rol')
                t['eliminar'] = False if len(md_servicio.Servicios.objects.filter(taxista_id = t['id'])) > 0 else True
            return list(taxistas)
        except Taxistas.DoesNotExist:
            return 'No existe el taxista'
        except Exception as e:
            return 'error'

    def guardar_taxi(self, json_data):
        ls_img_borrar = list()
        try:
            respuesta, usuario = self.persona.usuario.guardar_usuario(json_data, json_data['usuario__rol'])
            if respuesta == 'correo repetido':
                return respuesta
            if respuesta == 'otro rol':
                self.persona = md_usuario.Personas.objects.get(usuario_id = usuario.id)
            self.persona.usuario = usuario
            respuesta, persona = self.persona.guardar_persona(json_data)
            if len(md_usuario.RolesUsuario.objects.filter(usuario_id = usuario.id).select_related('rol').filter(Q(rol__nombre = 'Taxista formal') | Q(rol__nombre = 'Taxista informal'))) == 0:
                roles = md_usuario.RolesUsuario()
                roles.usuario = usuario
                roles.rol = (md_usuario.Roles.objects.get(nombre = json_data['usuario__rol']))
                roles.save()
            if 'disponibilidad' in json_data:
                self.disponibilidad = json_data['disponibilidad']
            if 'numero_placa' in json_data:
                self.numero_placa = json_data['numero_placa']
            self.persona = persona
            self.save()
            taxista = Taxistas.objects.filter(id = self.id).select_related('persona').values('foto_cedula_f', 'foto_cedula_t', 'foto_vehiculo', 'foto_matricula_f', 'foto_matricula_t', 'foto_licencia_f', 'foto_licencia_t', 'persona__foto_perfil')
            for campo in ls_campos:
                if campo in json_data:
                    if(taxista[0][campo] != ''):
                        ls_img_borrar.append('media/'+ taxista[0][campo])
                    file.base64 = json_data[campo]
                    file.nombre_file = campo + '_' + str(usuario.id)
                    if 'foto_cedula_f' == campo:
                        self.foto_cedula_f = file.get_file()
                    if 'foto_cedula_t' == campo:
                        self.foto_cedula_t = file.get_file()
                    if 'foto_vehiculo' == campo:
                        self.foto_vehiculo = file.get_file()
                    if 'foto_matricula_f' == campo:
                        self.foto_matricula_f = file.get_file()
                    if 'foto_matricula_t' == campo:
                        self.foto_matricula_t = file.get_file()
                    if 'foto_licencia_f' == campo:
                        self.foto_licencia_f = file.get_file()
                    if 'foto_licencia_t' == campo:
                        self.foto_licencia_t = file.get_file()
                    if 'persona__foto_perfil' == campo:
                        file.nombre_file = 'usuario_' + str(usuario.id)
                        self.persona.foto_perfil = file.get_file()
                        self.persona.save()  
            self.save()  
            # Si el taxista es registrado por una cooperativa
            if 'id_cooperativa' in json_data:
                cooperativa = md_cooperativa.Cooperativas.objects.get(pk = int(json_data['id_cooperativa']))
                coopTaxi = md_cooperativa.CoopeTaxis()
                coopTaxi.cooperativa = cooperativa
                coopTaxi.taxista = self
                coopTaxi.save()
            for ruta_file in ls_img_borrar:
                os.remove(ruta_file)
            return 'guardado'
        except Exception as e: 
            return 'error' 

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
                    self.eliminar_fotos_taxi()
                    persona.delete()
                    usuario.delete()
                else:
                    # Se elimina sólo el rol de Taxista del usuario, porque tiene otros roles como: Cliente o Administrador
                    rol_usuario = md_usuario.RolesUsuario.objects.get(id = roles.get(Q(rol__nombre = 'Taxista formal') | Q(rol__nombre = 'Taxista informal'))['id'])
                    rol_usuario.delete()
                    self.delete()
                    self.eliminar_fotos_taxi()
                return 'eliminado'
        except Exception as e: 
            return 'error'

     
    def eliminar_fotos_taxi(self):
        try:
            os.remove(self.foto_cedula_f.url[1:])
            os.remove(self.foto_cedula_t.url[1:])
            os.remove(self.foto_vehiculo.url[1:])
            os.remove(self.foto_matricula_f.url[1:])
            os.remove(self.foto_matricula_t.url[1:])
            os.remove(self.foto_licencia_f.url[1:])
            os.remove(self.foto_licencia_t.url[1:])
            return True
        except Exception as e: 
            return False

