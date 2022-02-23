from django.urls import path
from Usuario import views

urlpatterns = [
    path('', views.Usuario.as_view()),
]