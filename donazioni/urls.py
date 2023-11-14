from django.urls import path
from . import views

urlpatterns = [
    path('donazioni', views.donazioni, name="donazioni"),
    path('donazioni/salva/', views.salva, name="salva_donazione"),
    path('donazioni/esporta/', views.esporta, name="esporta_donazioni"),
    path('donazioni/storico/', views.storico, name="storico_donazioni"),
    path('donazioni/modifica/', views.modifica, name="modifica_donazione"),
    path('donazioni/aggiungi/', views.aggiungi, name="aggiungi_donazione"),
    path('donazioni/download/<int:dId>/', views.download, name="download_esame"),
]
