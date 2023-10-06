from django.urls import path
from . import views


urlpatterns = [
    path('donatori/', views.donatori, name="donatori"),
    path('donatori/salva/', views.salva, name="salva_donatore"),
    path('donatori/modifica/', views.modifica, name="modifica_donatore"),
    path('donatori/esporta/', views.esporta, name="esporta_donatori"),
    path('donatori/aggiungi/', views.aggiungi, name="aggiungi_donatore"),
    path('donatori/elimina/', views.elimina, name="elimina_donatore"),
]
