from django.urls import path
from Cooperativa import views

urlpatterns = [
    path('', views.Cooperativa.as_view()),
]