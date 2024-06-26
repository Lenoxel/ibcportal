# Generated by Django 3.0.4 on 2020-05-01 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200430_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='video',
            name='src',
            field=models.CharField(blank=True, max_length=100, verbose_name='URL'),
        ),
    ]
