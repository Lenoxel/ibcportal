# Generated by Django 3.0.4 on 2021-12-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20211227_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='filho', to='core.Member', verbose_name='Filhos'),
        ),
    ]