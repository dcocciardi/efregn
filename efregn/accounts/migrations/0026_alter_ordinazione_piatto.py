# Generated by Django 4.2.6 on 2024-01-24 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_alter_ordinazione_utente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordinazione',
            name='piatto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.piatto'),
        ),
    ]