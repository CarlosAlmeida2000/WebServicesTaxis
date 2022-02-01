from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.core.files.base import ContentFile
from Usuario.models import *
from .models import *
import json, base64, os

# Create your views here.
class Cooperativa(APIView):

    # GET con parámetros 
    # http://127.0.0.1:8000/cooperativa/?param=dato&param2=dato
    # GET sin parámetros
    # http://127.0.0.1:8000/cooperativa/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                cooperativas = Cooperativas.objects.all().select_related('persona')
                return Response({'cooperativa': list(cooperativas.values())})
            except Cooperativas.DoesNotExist:
                return Response({'cooperativa': 'No existe la cooperativa.'})
            except Exception as e:
                return Response({'cooperativa': 'Sucedió un error al obtener los datos, por favor intente nuevamente.'})
    

    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    usuario = Usuarios()
                    persona = Personas()
                    cooperativa = Cooperativas()
                    if cooperativa.guardar_coop(json_data, usuario, persona):
                        return Response({'cooperativa': True})
                    return Response({'cooperativa': False})
            except Exception as e: 
                return Response({'cooperativa': False})

    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    cooperativa = Cooperativas.objects.get(id = json_data['cooperativa_id'])
                    persona = Personas.objects.get(id = cooperativa.persona.id)
                    usuario = Usuarios.objects.get(id = persona.usuario.id)
                    if cooperativa.guardar_coop(json_data, usuario, persona):
                        return Response({'cooperativa': True})
                    return Response({'cooperativa': False})
            except Exception as e: 
                return Response({'cooperativa': False})

  
