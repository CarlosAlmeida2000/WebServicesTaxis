from rest_framework.views import APIView
from rest_framework.response import Response
from Usuario.models import *
from .models import *
import json

# Create your views here.
class Taxista(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                taxistas = Taxistas.obtener_taxis(request)
                return Response({'taxista': taxistas})
            except Exception as e:
                return Response({'taxista': 'error'})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                taxista = Taxistas()
                persona = Personas()
                usuario = Usuarios()
                persona.usuario = usuario
                taxista.persona = persona
                return Response({'taxista': taxista.guardar_taxi(json_data)})
            except Exception as e: 
                return Response({'taxista': 'error'})

    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                taxista = Taxistas.objects.get(id = json_data['id'])
                return Response({'taxista': taxista.guardar_taxi(json_data)})
            except Exception as e: 
                return Response({'taxista': 'error'})

    def delete(self, request, format = None):
        if request.method == 'DELETE':
            try:
                taxista = Taxistas.objects.get(id = request.GET['id'])
                return Response({'taxista': taxista.eliminar_taxi()})
            except Exception as e: 
                return Response({'taxista': 'error'})
