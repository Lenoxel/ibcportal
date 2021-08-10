# Generated by Django 3.0.4 on 2021-08-10 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20210810_1157'),
        ('groups', '0009_generalcategory_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='another_leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='another_group_leader', to='core.Member', verbose_name='Outro líder'),
        ),
        migrations.AddField(
            model_name='group',
            name='another_vice_leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='another_vice_leader', to='core.Member', verbose_name='Outro vice-líder'),
        ),
        migrations.AddField(
            model_name='groupmeetingdate',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Tipo do encontro'),
        ),
    ]
