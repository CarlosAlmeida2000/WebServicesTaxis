from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import json

# Create your views here.
class Usuario(APIView):

    # GET con parámetros 
    # http://127.0.0.1:8000/usuario/?param=dato&param2=dato
    # GET sin parámetros
    # http://127.0.0.1:8000/usuario/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                usuarios = list(Usuarios.objects.all().values())
                return Response({"usuarios": usuarios})
            except Usuarios.DoesNotExist:
                return Response({"mensaje": "No existe el usuario."})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})