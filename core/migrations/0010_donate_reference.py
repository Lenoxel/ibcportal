# Generated by Django 3.0.4 on 2020-04-12 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200412_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='donate',
            name='reference',
            field=models.CharField(default=0, max_length=20, verbose_name='Referência'),
            preserve_default=False,
        ),
    ]
