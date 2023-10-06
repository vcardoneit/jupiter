from django.urls import path
from . import views

urlpatterns = [
    path('avvisi/', views.avvisi, name="avvisi"),
]
