from django.db import models
from fernet_fields import EncryptedTextField
from django.db import IntegrityError
from Usuario.File import File
import os

# Create your models here.
class Roles(models.Model):
    nombre = models.CharField(max_length = 16)

class Usuarios(models.Model):
    correo = models.EmailField(max_length = 75, unique = True)
    clave = EncryptedTextField()
    habilitado = models.BooleanField(default = True)
    conf_correo = models.BooleanField(default = True)

    def guardar_usuario(self, json_data, rol_usuario):
        try:
            if 'persona__usuario__correo' in json_data:
                self.correo = json_data['persona__usuario__correo']
            if 'persona__usuario__clave' in json_data:
                self.clave = json_data['persona__usuario__clave']
            if 'persona__usuario__habilitado' in json_data:
                self.habilitado = json_data['persona__usuario__habilitado']
            self.save()
            return 'si', self
        except IntegrityError:
            # Verificar si ese usuario repetido tiene el rol especificado por parámetro, de lo contrario tiene otro rol y se continua con el registro
            self = Usuarios.objects.get(correo = self.correo)
            roles = RolesUsuario.objects.filter(usuario_id = self.id).select_related('rol').filter(rol__nombre = rol_usuario)
            if len(roles) > 0:
                return 'correo repetido', None
            else:
                return 'otro rol', self
 
class RolesUsuario(models.Model):
    usuario = models.ForeignKey('Usuario.Usuarios', on_delete = models.PROTECT, related_name = 'usuarios')
    rol = models.ForeignKey('Usuario.Roles', on_delete = models.PROTECT, related_name = 'roles')

class Personas(models.Model):
    nombres = models.CharField(max_length = 40)
    apellidos = models.CharField(max_length = 40)
    cedula = models.CharField(max_length = 10)
    telefono = models.CharField(max_length = 10)
    foto_perfil = models.ImageField(upload_to = 'Perfiles', null = True, blank = True)
    usuario = models.OneToOneField('Usuario.Usuarios', on_delete = models.PROTECT)

    def guardar_persona(self, json_data):
        try:
            if 'persona__nombres' in json_data:
                self.nombres = json_data['persona__nombres']
            if 'persona__apellidos' in json_data:
                self.apellidos = json_data['persona__apellidos']
            if 'persona__cedula' in json_data:
                self.cedula = json_data['persona__cedula']
            if 'persona__telefono' in json_data:
                self.telefono = json_data['persona__telefono']
            if 'persona__foto_perfil' in json_data and json_data['persona__foto_perfil'] != '':
                ruta_img_borrar = ''
                if(str(self.foto_perfil) != ''):
                    ruta_img_borrar = self.foto_perfil.url[1:]
                file = File()
                file.base64 = json_data['persona__foto_perfil']
                file.nombre_file = 'usuario_' + str(self.usuario.id)
                self.foto_perfil = file.get_file()
                if(ruta_img_borrar != ''):
                    os.remove(ruta_img_borrar)
            self.usuario = self.usuario
            self.save()
            return 'si', self
        except Exception as e: 
            return 'error', None

