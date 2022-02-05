from django.db import models
from fernet_fields import EncryptedTextField

# Create your models here.
class Roles(models.Model):
    nombre = models.CharField(max_length = 16)

class Usuarios(models.Model):
    correo = models.EmailField(max_length = 75, unique = True)
    clave = EncryptedTextField()
    habilitado = models.BooleanField(default = True)
    conf_correo = models.BooleanField(default = True)
 
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