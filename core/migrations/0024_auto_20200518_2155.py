# Generated by Django 3.0.4 on 2020-05-19 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_audit_obj_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, max_length=800, null=True, verbose_name='Descrição do vídeo'),
        ),
    ]
