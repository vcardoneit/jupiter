# Generated by Django 4.2.5 on 2023-10-21 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donatori', '0006_alter_donatori_fototessera'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatori',
            name='qrverify',
            field=models.CharField(default='', max_length=32),
        ),
    ]
