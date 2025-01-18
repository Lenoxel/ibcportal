# Generated by Django 3.0.4 on 2021-12-29 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0042_auto_20211227_1253"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="embed_code",
            field=models.TextField(
                blank=True, null=True, verbose_name="Código de incorporação do vídeo"
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="youtube_video_code",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Código do Youtube"
            ),
        ),
    ]
