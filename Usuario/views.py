
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
                usuarios = list(Usuarios.objects.all().values('id', 'correo', 'habilitado', 'conf_correo'))
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
                if(usuario.clave == json_data['clave']):
                    file = File()
                    roles = RolesUsuario.objects.filter(usuario__id = usuario.pk).select_related('rol')
                    
                    array_roles = []
                    for r in roles:
                        if r.rol.nombre == 'Administrador':
                            array_roles.append({'rol': r.rol.nombre})
                        if r.rol.nombre == 'Cooperativa':
                            array_roles.append({
                                'rol': r.rol.nombre,
                                'cooperativa_id': usuario.personas.cooperativas.id,
                                'nom_cooperativa': usuario.personas.cooperativas.nom_cooperativa,
                                'telefono': usuario.personas.cooperativas.telefono,
                                'direccion': usuario.personas.cooperativas.direccion,
                                'ingresar_cobro': usuario.personas.cooperativas.ingresar_cobro,
                            })
                        if r.rol.nombre == 'Cliente':
                            array_roles.append({
                                'rol': r.rol.nombre,
                                'cliente_id': usuario.personas.clientes.id
                            })
                        if r.rol.nombre == 'Taxista formal' or r.rol.nombre == 'Taxista informal':
                            file.ruta = usuario.personas.taxistas.foto_cedula_f
                            foto_cedula_f = file.get_base64()

                            file.ruta = usuario.personas.taxistas.foto_cedula_t
                            foto_cedula_t = file.get_base64()

                            file.ruta = usuario.personas.taxistas.foto_vehiculo
                            foto_vehiculo = file.get_base64()

                            file.ruta = usuario.personas.taxistas.foto_matricula_f
                            foto_matricula_f = file.get_base64()

                            file.ruta = usuario.personas.taxistas.foto_matricula_t
                            foto_matricula_t = file.get_base64()

                            file.ruta = usuario.personas.taxistas.foto_licencia_f
                            foto_licencia_f = file.get_base64()

                            file.ruta = usuario.personas.taxistas.foto_licencia_t
                            foto_licencia_t = file.get_base64()

                            array_roles.append({
                                'rol': r.rol.nombre,
                                'taxista_id': usuario.personas.taxistas.id,
                                'foto_cedula_f': foto_cedula_f,
                                'foto_cedula_t': foto_cedula_t,
                                'foto_vehiculo': foto_vehiculo,
                                'foto_matricula_f': foto_matricula_f,
                                'foto_matricula_t': foto_matricula_t,
                                'foto_licencia_f': foto_licencia_f,
                                'foto_licencia_t': foto_licencia_t,
                                'numero_placa': usuario.personas.taxistas.numero_placa,
                                'disponibilidad': usuario.personas.taxistas.disponibilidad
                            })

                    file.ruta = usuario.personas.foto_perfil
                    json_usuario = {
                            'persona_id': usuario.personas.id,
                            'persona__nombres': usuario.personas.nombres,
                            'persona__apellidos': usuario.personas.apellidos,
                            'persona__cedula': usuario.personas.cedula,
                            'persona__telefono': usuario.personas.telefono, 
                            'persona__foto_perfil': file.get_base64(),
                            'persona__usuario_id': usuario.pk,
                            'persona__usuario__correo': usuario.correo,
                            'persona__usuario__habilitado': usuario.habilitado,
                            'roles': array_roles
                            }
                    return Response({'usuario': json_usuario})
                else:
                    return Response({})
            except Usuarios.DoesNotExist:
                return Response({})
            except Exception as e:  
                return Response({})
    