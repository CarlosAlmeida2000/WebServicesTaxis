
from rest_framework.views import APIView
from rest_framework.response import Response
from Usuario.File import File
from .models import *
import json

# Create your views here.
class Usuario(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                usuarios = list(Usuarios.objects.all().values('id', 'correo', 'habilitado', 'conf_correo', 'clave'))
                return Response({'usuario': usuarios})
            except Usuarios.DoesNotExist:
                return Response({'usuario': 'No existe el usuario.'})
            except Exception as e:
                return Response({'usuario': 'Sucedió un error al obtener los datos, por favor intente nuevamente.'})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                usuario = Usuarios.objects.get(correo = json_data['correo'])
                if(usuario.habilitado != False):
                    if(usuario.clave == json_data['clave']):
                        file = File()
                        file.ruta = usuario.personas.foto_perfil
                        roles = RolesUsuario.objects.filter(usuario__id = usuario.pk).select_related('rol')
                        json_usuario = {'id': usuario.pk,
                                'correo': usuario.correo,
                                'nombres': usuario.personas.nombres,
                                'apellidos': usuario.personas.apellidos,
                                'cedula': usuario.personas.cedula,
                                'foto_perfil': file.get_base64(),
                                'roles': roles.values('rol__nombre')}
                        return Response({'usuario': json_usuario})
                    else:
                        return Response({'usuario': 'Credenciales incorrectas'})
                else:
                    return Response({'usuario': 'El usuario se encuentra deshabilitado'})
            except Usuarios.DoesNotExist:
                return Response({'usuario': 'No existe el usuario'})
            except Exception as e:  
                return Response({'usuario': 'error'})
    