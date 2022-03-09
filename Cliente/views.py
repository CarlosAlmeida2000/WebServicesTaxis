from rest_framework.views import APIView
from rest_framework.response import Response
from Usuario.models import *
from .models import *
import json

# Create your views here.
class Cliente(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                clientes = Clientes.obtener_clientes(request)
                return Response({'cliente': clientes})
            except Exception as e:
                return Response({'cliente': 'error'})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                cliente = Clientes()
                persona = Personas()
                usuario = Usuarios()
                persona.usuario = usuario
                cliente.persona = persona
                return Response({'cliente': cliente.guardar_cliente(json_data)})
            except Exception as e: 
                return Response({'cliente': 'error'})

    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                cliente = Clientes.objects.get(id = json_data['id'])
                return Response({'cliente': cliente.guardar_cliente(json_data)})
            except Exception as e: 
                return Response({'cliente': 'error'})
   