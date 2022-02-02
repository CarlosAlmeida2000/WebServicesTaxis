from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import json

# Create your views here.
class Usuario(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                usuarios = list(Usuarios.objects.all().values())
                return Response({'usuario': usuarios})
            except Usuarios.DoesNotExist:
                return Response({'usuario': 'No existe el usuario.'})
            except Exception as e:
                return Response({'usuario': 'Sucedió un error al obtener los datos, por favor intente nuevamente.'})