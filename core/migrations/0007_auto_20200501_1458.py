# Generated by Django 3.0.4 on 2020-05-01 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200501_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventinterests',
            options={'ordering': ['-interested_people_count'], 'verbose_name': 'Pessoas Interessas', 'verbose_name_plural': 'Pessoas Interessas em Eventos'},
        ),
    ]
