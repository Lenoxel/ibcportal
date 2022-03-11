# Generated by Django 3.0.4 on 2022-03-06 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebd', '0008_auto_20220222_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='EBDLabelOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Label')),
                ('type', models.CharField(blank=True, choices=[('positive', 'Positivo'), ('negative', 'Negativo'), ('neutral', 'Neutro')], max_length=30, null=True, verbose_name='Tipo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
            ],
            options={
                'verbose_name': 'Label de EBD',
                'verbose_name_plural': 'Labels de EBD',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='EBDPresenceRecordLabels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('ebd_label_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ebd_label_option', to='ebd.EBDLabelOptions', verbose_name='Label')),
                ('ebd_presence_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ebd_presence_record', to='ebd.EBDPresenceRecord', verbose_name='Registro de Presença')),
            ],
            options={
                'verbose_name': 'Label de aluno na EBD',
                'verbose_name_plural': 'Labels dos alunos na EBD',
                'ordering': ['-last_updated_date'],
            },
        ),
    ]