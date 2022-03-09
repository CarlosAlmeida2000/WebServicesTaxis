from rest_framework.views import APIView
from rest_framework.response import Response
from Usuario.models import *
from .models import *
import json

# Create your views here.
class Cooperativa(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                cooperativas = Cooperativas.obtener_coop(request)
                return Response({'cooperativa': cooperativas})
            except Exception as e:
                return Response({'cooperativa': 'error'})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                cooperativa = Cooperativas()
                persona = Personas()
                usuario = Usuarios()
                persona.usuario = usuario
                cooperativa.persona = persona
                return Response({'cooperativa': cooperativa.guardar_coop(json_data)})
            except Exception as e: 
                return Response({'cooperativa': 'error'})

    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                cooperativa = Cooperativas.objects.get(id = json_data['id'])
                return Response({'cooperativa': cooperativa.guardar_coop(json_data)})
            except Exception as e: 
                return Response({'cooperativa': 'error'})

    def delete(self, request, format = None):
        if request.method == 'DELETE':
            try:
                cooperativa = Cooperativas.objects.get(id = request.GET['id'])
                return Response({'cooperativa': cooperativa.eliminar_coop()})
            except Exception as e: 
                return Response({'cooperativa': 'error'})

  
