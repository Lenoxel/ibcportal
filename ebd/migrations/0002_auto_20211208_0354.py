# Generated by Django 3.0.4 on 2021-12-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0037_auto_20211208_0334"),
        ("ebd", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ebdclass",
            name="description",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Descrição"
            ),
        ),
        migrations.AlterField(
            model_name="ebdclass",
            name="secretaries",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="Secretário",
                to="core.Member",
                verbose_name="Secretário",
            ),
        ),
        migrations.AlterField(
            model_name="ebdclass",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="Aluno",
                to="core.Member",
                verbose_name="Aluno",
            ),
        ),
        migrations.AlterField(
            model_name="ebdclass",
            name="teachers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="Professor",
                to="core.Member",
                verbose_name="Professor",
            ),
        ),
    ]
