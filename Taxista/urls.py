from django.contrib import admin
from django.urls import path
from Taxista import views

urlpatterns = [
    path('', views.Taxista.as_view()),
]