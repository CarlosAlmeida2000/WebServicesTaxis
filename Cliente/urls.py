from django.urls import path
from Cliente import views

urlpatterns = [
    path('', views.Cliente.as_view()),
]