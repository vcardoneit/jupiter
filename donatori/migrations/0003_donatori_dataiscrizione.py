# Generated by Django 4.2.5 on 2023-10-08 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donatori', '0002_donatori_fenotipo_donatori_kell'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatori',
            name='dataiscrizione',
            field=models.DateField(null=True),
        ),
    ]
