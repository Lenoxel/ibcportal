# Generated by Django 3.0.4 on 2020-05-12 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0021_auto_20200511_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changed_model', models.CharField(max_length=50, verbose_name='Modelo modificado')),
                ('action_type', models.CharField(max_length=20, verbose_name='Ação')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('responsible', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Responsável')),
            ],
            options={
                'verbose_name': 'Auditoria',
                'verbose_name_plural': 'Auditorias',
                'ordering': ['-creation_date'],
            },
        ),
    ]
