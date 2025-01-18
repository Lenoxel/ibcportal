# Generated by Django 3.0.4 on 2021-12-08 06:39

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0037_auto_20211208_0334"),
    ]

    operations = [
        migrations.CreateModel(
            name="EBDClass",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Nome")),
                (
                    "description",
                    models.CharField(max_length=200, verbose_name="Descrição"),
                ),
                (
                    "background_image",
                    cloudinary.models.CloudinaryField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Imagem da turma",
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "last_updated_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Última modificação"
                    ),
                ),
                (
                    "church",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.Church",
                        verbose_name="Igreja",
                    ),
                ),
                (
                    "secretaries",
                    models.ManyToManyField(related_name="Secretário", to="core.Member"),
                ),
                (
                    "students",
                    models.ManyToManyField(related_name="Aluno", to="core.Member"),
                ),
                (
                    "teachers",
                    models.ManyToManyField(related_name="Professor", to="core.Member"),
                ),
            ],
            options={
                "verbose_name": "Turma",
                "verbose_name_plural": "Turmas",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="EBDClassLesson",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Lição")),
                ("date", models.DateField(verbose_name="Data da aula")),
                (
                    "number",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Número da aula"
                    ),
                ),
                (
                    "apply_to_all",
                    models.BooleanField(
                        default=True, verbose_name="Aplicar lição a todas as classes"
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "last_updated_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Última modificação"
                    ),
                ),
                (
                    "ebd_class",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ebd.EBDClass",
                        verbose_name="Turma",
                    ),
                ),
            ],
            options={
                "verbose_name": "Aula",
                "verbose_name_plural": "Aulas",
                "ordering": ["-date"],
            },
        ),
    ]
