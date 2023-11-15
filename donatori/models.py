import secrets
from django.db import models


class donatori(models.Model):
    tessera = models.AutoField(auto_created=True, primary_key=True)
    qrverify = models.CharField(max_length=32, default='')
    dataiscrizione = models.DateField(null=True)
    grupposang = models.CharField(max_length=3)
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
    privacy_a = models.BooleanField(default=False)
    privacy_b = models.BooleanField(default=False)
    privacy_c = models.BooleanField(default=False)
    modReferti = models.CharField(max_length=255, default='')
    autorizzazione = models.ImageField(upload_to='autorizzazioni/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qrverify:
            self.qrverify = secrets.token_hex(16)
        super().save(*args, **kwargs)
