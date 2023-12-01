from django.db import models


class prenotazioni(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    nome = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    data = models.DateField(null=True)
    primadonazione = models.CharField(max_length=255)
