from django.urls import path
from . import views

urlpatterns = [
    path('statistiche/', views.statistiche, name="statistiche"),
    path('statistiche/ricerca', views.ricerca, name="ricerca"),
]
