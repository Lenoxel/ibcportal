# Generated by Django 3.0.4 on 2020-04-12 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('background_image', models.ImageField(upload_to='group_images/', verbose_name='Imagem do grupo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Church', verbose_name='Igreja')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
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
            ],
            options={
                'verbose_name': 'Postagem',
                'verbose_name_plural': 'Postagens',
                'ordering': ['-last_updated_date'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(max_length=300, verbose_name='Descrição')),
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
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=100, verbose_name='URL')),
                ('category', models.CharField(choices=[('DOUTRINA', 'Culto de Doutrina'), ('EBD', 'Escola Bíblica Dominical'), ('INTERCESSAO', 'Culto de Intercessão'), ('DOMINGO', 'Culto de Domingo')], max_length=15, verbose_name='Categoria')),
                ('title', models.CharField(max_length=100, verbose_name='Título do vídeo')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição do vídeo')),
                ('registering_date', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
            ],
            options={
                'verbose_name': 'Vídeo',
                'verbose_name_plural': 'Vídeos',
                'ordering': ['-registering_date'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('DOUTRINA', 'Culto de Doutrina'), ('EBD', 'Escola Bíblica Dominical'), ('INTERCESSAO', 'Culto de Intercessão'), ('DOMINGO', 'Culto de Domingo')], max_length=15, verbose_name='Encontro')),
                ('start_date', models.DateTimeField(verbose_name='Horário de início')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Horário de fim')),
                ('description', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descrição')),
                ('category', models.CharField(choices=[('PRESENCIAL', 'Presencial'), ('ONLINE', 'Online')], max_length=15, verbose_name='Tipo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Church', verbose_name='Local')),
                ('organizing_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Group', verbose_name='Grupo Organizador')),
                ('preacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Publisher', verbose_name='Pregador')),
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
                'verbose_name': 'Visualização',
                'verbose_name_plural': 'Visualizações',
                'ordering': ['-views_count'],
            },
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='post_files/', verbose_name='Arquivo')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='core.Post', verbose_name='Postagem')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Publisher', verbose_name='Publicador'),
        ),
        migrations.AddField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_leader', to='core.Publisher', verbose_name='Líder'),
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
        migrations.AddField(
            model_name='church',
            name='chief_pastor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Publisher', verbose_name='Pastor Principal'),
        ),
    ]
