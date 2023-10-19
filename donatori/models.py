from django.db import models


class donatori(models.Model):
    tessera = models.AutoField(auto_created=True, primary_key=True)
    dataiscrizione = models.DateField(null=True)
    grupposang = models.CharField(max_length=3)
    fenotipo = models.CharField(max_length=255)
    kell = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    datadinascita = models.DateField(null=True)
    luogodinascita = models.CharField(max_length=255)
    codicefiscale = models.CharField(max_length=16)
    indirizzo = models.CharField(max_length=255)
    comune = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    email = models.EmailField()
    fototessera = models.ImageField(upload_to='fototessere/', default='default.jpg')
