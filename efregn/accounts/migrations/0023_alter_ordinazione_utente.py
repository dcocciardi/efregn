# Generated by Django 4.2.6 on 2024-01-24 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0022_alter_ordinazione_utente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordinazione',
            name='utente',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
