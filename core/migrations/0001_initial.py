# Generated by Django 3.0.4 on 2020-04-29 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('address', models.CharField(max_length=250, verbose_name='Endereço')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
            ],
            options={
                'verbose_name': 'Igreja',
                'verbose_name_plural': 'Igrejas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_name', models.CharField(max_length=100, verbose_name='Nome')),
                ('donor_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('donate_type', models.CharField(choices=[('tithe', 'Dízimo'), ('offer', 'Oferta')], max_length=20, verbose_name='Tipo de Oferta')),
                ('payment_option', models.CharField(choices=[('deposit', 'Depósito'), ('pagseguro', 'PagSeguro'), ('paypal', 'Paypal')], max_length=20, verbose_name='Opção de Pagamento')),
                ('payment_status', models.CharField(choices=[('pending', 'Pendente'), ('done', 'Concluído'), ('excluded', 'Excluído')], default='pending', max_length=20, verbose_name='Status do Pagamento')),
                ('amount', models.FloatField(verbose_name='Valor')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
            ],
            options={
                'verbose_name': 'Doação',
                'verbose_name_plural': 'Doações',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('nickname', models.CharField(max_length=25, verbose_name='Conhecido como')),
                ('description', models.TextField(max_length=300, verbose_name='Descrição')),
                ('address', models.CharField(max_length=100, verbose_name='Endereço')),
                ('church_function', models.CharField(max_length=40, verbose_name='Função na Igreja')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Data de nascimento')),
                ('picture', models.ImageField(upload_to='pictures/', verbose_name='Foto')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
            ],
            options={
                'verbose_name': 'Membro',
                'verbose_name_plural': 'membros',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título da postagem')),
                ('text', models.TextField(verbose_name='Texto da postagem')),
                ('to_notify', models.BooleanField(default=False, verbose_name='Notificar')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('published_date', models.DateTimeField(blank=True, null=True, verbose_name='Publicado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Gerenciador')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Member', verbose_name='Publicador')),
            ],
            options={
                'verbose_name': 'Postagem',
                'verbose_name_plural': 'Postagens',
                'ordering': ['-last_updated_date'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=100, verbose_name='URL')),
                ('category', models.CharField(choices=[('doutrina', 'Culto de Doutrina'), ('ebd', 'Escola Bíblica Dominical'), ('intercessao', 'Culto de Intercessão'), ('domingo', 'Culto de Domingo'), ('ceia', 'Ceia do Senhor')], max_length=20, verbose_name='Categoria')),
                ('title', models.CharField(max_length=100, verbose_name='Título do vídeo')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição do vídeo')),
                ('youtube_video_code', models.CharField(max_length=150, verbose_name='Código do Youtube')),
                ('registering_date', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
            ],
            options={
                'verbose_name': 'Vídeo',
                'verbose_name_plural': 'Vídeos',
                'ordering': ['-registering_date'],
            },
        ),
        migrations.CreateModel(
            name='VideoView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views_count', models.IntegerField(default=0, verbose_name='Visualizações')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Post', verbose_name='Postagem')),
            ],
            options={
                'verbose_name': 'Visualização do Vídeo',
                'verbose_name_plural': 'Visualizações dos Vídeos',
                'ordering': ['-views_count'],
            },
        ),
        migrations.CreateModel(
            name='VideoReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claps_count', models.IntegerField(default=0, verbose_name='Gostei')),
                ('dislike_count', models.IntegerField(default=0, verbose_name='Não gostei')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Reação ao Vídeo',
                'verbose_name_plural': 'Reações aos vídeos',
                'ordering': ['-claps_count', '-dislike_count'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('doutrina', 'Culto de Doutrina'), ('ebd', 'Escola Bíblica Dominical'), ('intercessao', 'Culto de Intercessão'), ('domingo', 'Culto de Domingo'), ('ceia', 'Ceia do Senhor')], max_length=20, verbose_name='Encontro')),
                ('start_date', models.DateTimeField(verbose_name='Horário de início')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Horário de fim')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição')),
                ('category', models.CharField(choices=[('PRESENCIAL', 'Presencial'), ('ONLINE', 'Online')], max_length=15, verbose_name='Tipo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Church', verbose_name='Local')),
                ('organizing_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group', verbose_name='Grupo Organizador')),
                ('preacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Member', verbose_name='Pregador')),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Encontro',
                'verbose_name_plural': 'Agenda',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views_count', models.IntegerField(default=0, verbose_name='Visualizações')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Post', verbose_name='Postagem')),
            ],
            options={
                'verbose_name': 'Visualização da Postagem',
                'verbose_name_plural': 'Visualizações das Postagens',
                'ordering': ['-views_count'],
            },
        ),
        migrations.CreateModel(
            name='PostReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claps_count', models.IntegerField(default=0, verbose_name='Gostei')),
                ('dislike_count', models.IntegerField(default=0, verbose_name='Não gostei')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Post', verbose_name='Postagem')),
            ],
            options={
                'verbose_name': 'Reação ao Post',
                'verbose_name_plural': 'Reações aos Posts',
                'ordering': ['-claps_count', '-dislike_count'],
            },
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_file', models.FileField(upload_to='post_files/', verbose_name='Arquivo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='core.Post', verbose_name='Postagem')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Evento')),
                ('start_date', models.DateTimeField(verbose_name='Início')),
                ('end_date', models.DateTimeField(verbose_name='Término')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição')),
                ('event_type', models.CharField(max_length=30, verbose_name='Tipo do evento')),
                ('price', models.FloatField(verbose_name='Valor (R$)')),
                ('picture', models.ImageField(upload_to='event_images/', verbose_name='Imagem do evento')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Church', verbose_name='Local')),
                ('organizing_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group', verbose_name='Grupo Organizador')),
                ('preacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Member', verbose_name='Pregador')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['-start_date'],
            },
        ),
        migrations.AddField(
            model_name='church',
            name='chief_pastor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Member', verbose_name='Pastor Principal'),
        ),
    ]
