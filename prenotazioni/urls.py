from django.urls import path
from .views import addprt
from . import views


urlpatterns = [
    path('prenotazioni/', views.index, name="prenotazioni"),
    path('prenotazioni/conferma/', views.conferma, name="prenotazioni_conferma"),
    path('prenotazioni/elimina/', views.elimina, name="prenotazioni_elimina"),
    path('api/addprt/', addprt.as_view(), name='aggiungi_prenotazione_api'),
]
