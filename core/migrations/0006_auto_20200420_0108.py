# Generated by Django 3.0.4 on 2020-04-20 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200420_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_leader', to='core.Member', verbose_name='Líder'),
        ),
        migrations.AlterField(
            model_name='group',
            name='third_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third_leader', to='core.Member', verbose_name='Terceiro líder'),
        ),
        migrations.AlterField(
            model_name='group',
            name='vice_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vice_leader', to='core.Member', verbose_name='Vice-líder'),
        ),
    ]
