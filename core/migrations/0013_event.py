# Generated by Django 3.0.4 on 2020-04-26 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('core', '0012_auto_20200426_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Evento')),
                ('start_date', models.DateTimeField(verbose_name='Início')),
                ('end_date', models.DateTimeField(verbose_name='Término')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição')),
                ('event_type', models.CharField(max_length=30, verbose_name='Tipo do evento')),
                ('price', models.FloatField(verbose_name='Valor (R$)')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Church', verbose_name='Local')),
                ('organizing_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group', verbose_name='Grupo Organizador')),
                ('preacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Member', verbose_name='Pregador')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['-start_date'],
            },
        ),
    ]
