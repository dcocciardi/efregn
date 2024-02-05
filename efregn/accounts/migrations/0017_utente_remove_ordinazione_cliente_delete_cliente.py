# Generated by Django 4.2.6 on 2023-10-11 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0016_alter_piatto_immagine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=25, null=True)),
                ('cognome', models.CharField(max_length=25, null=True)),
                ('email', models.CharField(max_length=30, null=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Utenti',
            },
        ),
        migrations.RemoveField(
            model_name='ordinazione',
            name='cliente',
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
    ]