# Generated by Django 3.0.4 on 2020-04-29 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('background_image', models.ImageField(upload_to='group_images/', verbose_name='Imagem do grupo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Church', verbose_name='Igreja')),
                ('leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_leader', to='core.Member', verbose_name='Líder')),
                ('third_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third_leader', to='core.Member', verbose_name='Terceiro líder')),
                ('vice_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vice_leader', to='core.Member', verbose_name='Vice-líder')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'ordering': ['name'],
            },
        ),
    ]
