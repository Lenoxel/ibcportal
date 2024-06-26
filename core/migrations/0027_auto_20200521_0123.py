# Generated by Django 3.0.4 on 2020-05-21 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200521_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pushnotification',
            old_name='message',
            new_name='body',
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='failure_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Mensagens não enviadas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='multicast_id',
            field=models.CharField(default='default', max_length=200, verbose_name='ID único da mensagem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='success_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Mensagens enviadas'),
            preserve_default=False,
        ),
    ]
