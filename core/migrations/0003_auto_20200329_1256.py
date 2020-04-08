# Generated by Django 3.0.4 on 2020-03-29 15:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200329_0303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['-start_date'], 'verbose_name': 'Encontro', 'verbose_name_plural': 'Agenda'},
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='date',
        ),
        migrations.AddField(
            model_name='schedule',
            name='does_repeat',
            field=models.BooleanField(default=False, verbose_name='Se repete'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Horário de fim'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='location',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Local'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='repetition_quantity',
            field=models.IntegerField(default=0, verbose_name='Quantidade de repetições semanais'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Horário de início'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='category',
            field=models.CharField(choices=[('PRESENCIAL', 'Presencial'), ('ONLINE', 'Online')], max_length=15, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='title',
            field=models.CharField(choices=[('DOUTRINA', 'Culto de Doutrina'), ('EBD', 'Escola Bíblica Dominical'), ('INTERCESSAO', 'Culto de Intercessão'), ('DOMINGO', 'Culto de Domingo')], max_length=15, verbose_name='Encontro'),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('DOUTRINA', 'Culto de Doutrina'), ('EBD', 'Escola Bíblica Dominical'), ('INTERCESSAO', 'Culto de Intercessão'), ('DOMINGO', 'Culto de Domingo')], max_length=15, verbose_name='Categoria'),
        ),
    ]