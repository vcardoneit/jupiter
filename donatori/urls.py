from django.urls import path
from . import views


urlpatterns = [
    path('donatori', views.donatori, name="donatori"),
    path('donatori/salva', views.salva, name="salva"),
    path('donatori/esporta', views.esporta, name="esporta"),
]
