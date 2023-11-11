from django.db import models
from donatori.models import donatori


class donazioni(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    donatore = models.ForeignKey(donatori, on_delete=models.CASCADE)
    data = models.DateField(null=True)
    tipo = models.CharField(max_length=255)
