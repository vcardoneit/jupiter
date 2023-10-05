from django.urls import path
from . import views

urlpatterns = [
    path('donazioni', views.donazioni, name="donazioni"),
    path('donazioni/salva', views.salva, name="salva"),
    path('donazioni/esporta', views.esporta, name="esporta"),
]
