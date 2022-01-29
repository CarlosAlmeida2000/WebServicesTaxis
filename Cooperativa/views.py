from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import json

# Create your views here.
class Cooperativa(APIView):

    # GET con parámetros 
    # http://127.0.0.1:8000/cooperativa/?param=dato&param2=dato
    # GET sin parámetros
    # http://127.0.0.1:8000/cooperativa/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                cooperativas = list(Cooperativas.objects.all().values())
                return Response({"cooperativas": cooperativas})
            except Cooperativas.DoesNotExist:
                return Response({"mensaje": "No existe la cooperativa."})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})