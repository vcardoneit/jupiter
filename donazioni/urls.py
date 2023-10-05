from django.urls import path
from . import views

urlpatterns = [
    path('donazioni', views.donazioni, name="donazioni"),
    path('salvaDn', views.salvaDn, name="salvaDn"),
]
