# Generated by Django 3.0.4 on 2020-04-23 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200421_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='church',
        ),
        migrations.RemoveField(
            model_name='group',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='group',
            name='third_leader',
        ),
        migrations.RemoveField(
            model_name='group',
            name='vice_leader',
        ),
    ]
