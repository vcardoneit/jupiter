from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('tessera/', views.tessera, name="tessera"),
    path('autorizzazione/', views.autorizzazione, name="autorizzazione"),
    path('autorizzazione/download/<int:dId>/', views.autdownload, name="autdownload"),
    path('autorizza/', views.autorizza, name="autorizza"),
]
