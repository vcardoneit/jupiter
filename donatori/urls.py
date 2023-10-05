from django.urls import path
from . import views


urlpatterns = [
    path('donatori', views.donatori, name="donatori"),
    path('salvaTs', views.salvaTs, name="salvaTs"),
]
