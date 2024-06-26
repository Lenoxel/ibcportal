# Generated by Django 3.0.4 on 2020-04-29 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizing_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group', verbose_name='Grupo Organizador'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='organizing_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group', verbose_name='Grupo Organizador'),
        ),
    ]
