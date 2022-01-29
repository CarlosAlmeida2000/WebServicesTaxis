from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import json

# Create your views here.
class Taxista(APIView):

    # GET con parámetros 
    # http://127.0.0.1:8000/taxista/?param=dato&param2=dato
    # GET sin parámetros
    # http://127.0.0.1:8000/taxista/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                taxistas = list(Taxistas.objects.all().values())
                return Response({"taxistas": taxistas})
            except Taxistas.DoesNotExist:
                return Response({"mensaje": "No existe el taxista."})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})