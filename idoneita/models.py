from django.db import models


class idoneita(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    nominativo = models.CharField(max_length=255)
    dataprelievo = models.DateField(null=True)
    telefono = models.CharField(max_length=255)
    idoneo = models.CharField(max_length=255, default="In attesa")
