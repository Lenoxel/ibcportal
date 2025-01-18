# Generated by Django 3.0.4 on 2023-01-07 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ebd", "0016_auto_20220806_1231"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ebdlabeloptions",
            options={
                "ordering": ["title"],
                "verbose_name": "Etiqueta de EBD",
                "verbose_name_plural": "Etiquetas de EBD",
            },
        ),
        migrations.AlterModelOptions(
            name="ebdpresencerecordlabels",
            options={
                "ordering": ["-last_updated_date"],
                "verbose_name": "Etiqueta de aluno na EBD",
                "verbose_name_plural": "Etiquetas dos alunos na EBD",
            },
        ),
    ]
