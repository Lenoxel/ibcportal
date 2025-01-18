# Generated by Django 3.0.4 on 2020-06-24 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0009_generalcategory_icon"),
        ("core", "0031_auto_20200624_1308"),
    ]

    operations = [
        migrations.AddField(
            model_name="church",
            name="general_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="groups.GeneralCategory",
                verbose_name="Categoria",
            ),
        ),
    ]
