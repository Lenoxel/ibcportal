# Generated by Django 3.0.4 on 2020-05-31 05:30

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_auto_20200529_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalcategory',
            name='icon',
            field=cloudinary.models.CloudinaryField(default='default', max_length=255, verbose_name='Ícone da categoria'),
            preserve_default=False,
        ),
    ]
