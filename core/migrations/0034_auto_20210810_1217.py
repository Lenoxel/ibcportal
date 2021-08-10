# Generated by Django 3.0.4 on 2021-08-10 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0033_member_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='member',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='member',
            name='instagram',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='member',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='WhatsApp'),
        ),
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='member',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='title',
            field=models.CharField(choices=[('doutrina', 'Culto de Doutrina'), ('ebd', 'Escola Bíblica Dominical'), ('intercessao', 'Culto de Intercessão'), ('domingo', 'Culto de Domingo'), ('ceia', 'Ceia do Senhor'), ('casa', 'Cultuando em casa'), ('infantil', 'Culto Infantil'), ('oracao', 'Círculo de Oração'), ('domestico', 'Culto doméstico'), ('consagracao', 'Consagração'), ('geral', 'Geral')], max_length=20, verbose_name='Encontro'),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('doutrina', 'Culto de Doutrina'), ('ebd', 'Escola Bíblica Dominical'), ('intercessao', 'Culto de Intercessão'), ('domingo', 'Culto de Domingo'), ('ceia', 'Ceia do Senhor'), ('casa', 'Cultuando em casa'), ('infantil', 'Culto Infantil'), ('oracao', 'Círculo de Oração'), ('domestico', 'Culto doméstico'), ('consagracao', 'Consagração'), ('geral', 'Geral')], max_length=20, verbose_name='Categoria'),
        ),
    ]
