# Generated by Django 3.0.4 on 2020-05-21 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_notificationdevice_pushnotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushnotification',
            name='push_date',
            field=models.DateTimeField(verbose_name='Data do envio'),
        ),
    ]
