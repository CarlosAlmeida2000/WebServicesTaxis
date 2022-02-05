from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.core.files.base import ContentFile
from Usuario.models import *
from .models import *
import json, base64, os

# Create your views here.
class Taxista(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                taxistas = Taxistas.obtener_taxis(request)
                return Response({'taxista': taxistas})
            except Exception as e:
                return Response({'taxista': 'Sucedió un error al obtener los datos, por favor intente nuevamente.'})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                usuario = Usuarios()
                persona = Personas()
                taxista = Taxistas()
                if taxista.guardar_taxi(json_data, usuario, persona):
                    return Response({'taxista': True})
                return Response({'taxista': False})
            except Exception as e: 
                print(str(e))
                return Response({'taxista': False})

    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                taxista = Taxistas.objects.get(id = json_data['id'])
                persona = Personas.objects.get(id = taxista.persona.id)
                usuario = Usuarios.objects.get(id = persona.usuario.id)
                if taxista.guardar_taxi(json_data, usuario, persona):
                    return Response({'taxista': True})
                return Response({'taxista': False})
            except Exception as e: 
                return Response({'taxista': False})

    def delete(self, request, format=None):
        if request.method == 'DELETE':
            try:
                taxista = Taxistas.objects.get(id = request.GET['id'])
                if taxista.eliminar_taxi():
                    return Response({'taxista': True})
                return Response({'taxista': False})
            except Exception as e: 
                return Response({'taxista': False})
