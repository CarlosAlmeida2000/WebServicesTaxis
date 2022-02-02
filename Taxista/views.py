from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import json

# Create your views here.
class Taxista(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                taxistas = list(Taxistas.objects.all().values())
                return Response({'taxista': taxistas})
            except Taxistas.DoesNotExist:
                return Response({'taxista': 'No existe el taxista.'})
            except Exception as e:
                return Response({'taxista': 'Sucedió un error al obtener los datos, por favor intente nuevamente.'})