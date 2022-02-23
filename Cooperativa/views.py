from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.core.files.base import ContentFile
from Usuario.models import *
from .models import *
import json, base64, os

# Create your views here.
class Cooperativa(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                cooperativas = Cooperativas.obtener_coop(request)
                return Response({'cooperativa': cooperativas})
            except Exception as e:
                return Response({'cooperativa': 'Sucedió un error al obtener los datos, por favor intente nuevamente.'})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                usuario = Usuarios()
                persona = Personas()
                cooperativa = Cooperativas()
                return Response({'cooperativa': cooperativa.guardar_coop(json_data, usuario, persona)})
            except Exception as e: 
                return Response({'cooperativa': 'error'})

    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                cooperativa = Cooperativas.objects.get(id = json_data['id'])
                persona = Personas.objects.get(id = cooperativa.persona.id)
                usuario = Usuarios.objects.get(id = persona.usuario.id)
                return Response({'cooperativa': cooperativa.guardar_coop(json_data, usuario, persona)})
            except Exception as e: 
                return Response({'cooperativa': 'error'})

    def delete(self, request, format = None):
        if request.method == 'DELETE':
            try:
                cooperativa = Cooperativas.objects.get(id = request.GET['id'])
                return Response({'cooperativa': cooperativa.eliminar_coop()})
            except Exception as e: 
                return Response({'cooperativa': 'error'})

  
