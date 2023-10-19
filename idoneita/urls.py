from django.urls import path
from . import views

urlpatterns = [
    path('idoneita', views.idoneita, name="idoneita"),
    path('idoneita/modifica/', views.modifica, name="modifica_predonazione"),
    path('idoneita/aggiungi/', views.aggiungi, name="aggiungi_predonazione"),
    path('idoneita/salva/', views.salva, name="salva_predonazione"),
]
