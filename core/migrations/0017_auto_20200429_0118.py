# Generated by Django 3.0.4 on 2020-04-29 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200429_0115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='member',
            name='birthday_dayofyear_internal',
        ),
    ]
