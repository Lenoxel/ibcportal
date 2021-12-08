# Generated by Django 3.0.4 on 2021-12-08 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20210810_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='cep',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='CEP'),
        ),
        migrations.AddField(
            model_name='member',
            name='church_relation',
            field=models.CharField(blank=True, choices=[('membro', 'Membro'), ('congregado', 'Congregado')], max_length=20, null=True, verbose_name='Relação com a Igreja'),
        ),
        migrations.AddField(
            model_name='member',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Cidade'),
        ),
        migrations.AddField(
            model_name='member',
            name='district',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='member',
            name='ebd_relation',
            field=models.CharField(blank=True, choices=[('aluno', 'Aluno'), ('visitante', 'Visitante')], max_length=20, null=True, verbose_name='Relação com a EBD'),
        ),
        migrations.AddField(
            model_name='member',
            name='educational_level',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Grau de escolaridade'),
        ),
        migrations.AddField(
            model_name='member',
            name='marital_status',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Estado civil'),
        ),
        migrations.AddField(
            model_name='member',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='member',
            name='church_function',
            field=models.CharField(max_length=50, verbose_name='Função na Igreja'),
        ),
    ]
