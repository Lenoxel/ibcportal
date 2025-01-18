# Generated by Django 3.0.4 on 2020-05-12 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_auto_20200508_0024"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="title",
            field=models.CharField(
                choices=[
                    ("doutrina", "Culto de Doutrina"),
                    ("ebd", "Escola Bíblica Dominical"),
                    ("intercessao", "Culto de Intercessão"),
                    ("domingo", "Culto de Domingo"),
                    ("ceia", "Ceia do Senhor"),
                    ("casa", "Cultuando em casa"),
                    ("infantil", "Culto Infantil"),
                    ("oracao", "Ciclo de Oração"),
                    ("domestico", "Culto doméstico"),
                    ("geral", "Geral"),
                ],
                max_length=20,
                verbose_name="Encontro",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="category",
            field=models.CharField(
                choices=[
                    ("doutrina", "Culto de Doutrina"),
                    ("ebd", "Escola Bíblica Dominical"),
                    ("intercessao", "Culto de Intercessão"),
                    ("domingo", "Culto de Domingo"),
                    ("ceia", "Ceia do Senhor"),
                    ("casa", "Cultuando em casa"),
                    ("infantil", "Culto Infantil"),
                    ("oracao", "Ciclo de Oração"),
                    ("domestico", "Culto doméstico"),
                    ("geral", "Geral"),
                ],
                max_length=20,
                verbose_name="Categoria",
            ),
        ),
    ]
