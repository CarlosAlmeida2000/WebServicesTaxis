import imp
from django.contrib import admin
from django.urls import path
from Usuario import views

urlpatterns = [
    path('', views.Usuario.as_view()),
]