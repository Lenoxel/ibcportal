# Generated by Django 3.0.4 on 2020-05-08 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200504_2350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postfile',
            options={'ordering': ['post_file'], 'verbose_name': 'Arquivo', 'verbose_name_plural': 'Arquivos'},
        ),
    ]
