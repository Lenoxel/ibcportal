# Generated by Django 3.0.4 on 2020-03-29 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['-date'], 'verbose_name': 'Encontro', 'verbose_name_plural': 'Agenda'},
        ),
        migrations.AddField(
            model_name='group',
            name='third_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third_leader', to='core.Publisher', verbose_name='Terceiro líder'),
        ),
        migrations.AddField(
            model_name='group',
            name='vice_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vice_leader', to='core.Publisher', verbose_name='Vice-líder'),
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_leader', to='core.Publisher', verbose_name='Líder'),
        ),
    ]
