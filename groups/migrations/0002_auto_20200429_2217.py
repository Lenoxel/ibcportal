# Generated by Django 3.0.4 on 2020-04-30 01:17

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="background_image",
            field=cloudinary.models.CloudinaryField(
                max_length=255, verbose_name="Imagem do grupo"
            ),
        ),
    ]
