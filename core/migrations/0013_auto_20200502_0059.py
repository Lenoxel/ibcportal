# Generated by Django 3.0.4 on 2020-05-02 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200502_0017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membersunion',
            options={'ordering': ['-union_date'], 'verbose_name': 'União', 'verbose_name_plural': 'Uniões'},
        ),
        migrations.AlterField(
            model_name='membersunion',
            name='man',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='man', to='core.Member', verbose_name='Homem'),
        ),
        migrations.AlterField(
            model_name='membersunion',
            name='woman',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='woman', to='core.Member', verbose_name='Mulher'),
        ),
    ]