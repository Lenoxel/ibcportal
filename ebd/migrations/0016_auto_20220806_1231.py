# Generated by Django 3.0.4 on 2022-08-06 15:31

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20220519_0208'),
        ('ebd', '0015_ebdlessonclassdetails'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ebdclass',
            options={'ordering': ['name'], 'verbose_name': 'Classe', 'verbose_name_plural': 'Classes'},
        ),
        migrations.AlterModelOptions(
            name='ebdlesson',
            options={'ordering': ['-date'], 'verbose_name': 'Lição', 'verbose_name_plural': 'Lições'},
        ),
        migrations.AddField(
            model_name='ebdlesson',
            name='single_class',
            field=models.BooleanField(default=False, verbose_name='Classe Única'),
        ),
        migrations.AlterField(
            model_name='ebdclass',
            name='background_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Imagem da classe'),
        ),
        migrations.AlterField(
            model_name='ebdclass',
            name='secretaries',
            field=models.ManyToManyField(blank=True, related_name='secretary', to='core.Member', verbose_name='Secretários'),
        ),
        migrations.AlterField(
            model_name='ebdclass',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student', to='core.Member', verbose_name='Alunos'),
        ),
        migrations.AlterField(
            model_name='ebdclass',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='teacher', to='core.Member', verbose_name='Professores'),
        ),
        migrations.AlterField(
            model_name='ebdlesson',
            name='date',
            field=models.DateField(verbose_name='Data da lição'),
        ),
        migrations.AlterField(
            model_name='ebdlesson',
            name='ebd_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ebd.EBDClass', verbose_name='Classe'),
        ),
        migrations.AlterField(
            model_name='ebdlesson',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Número da lição'),
        ),
    ]
