# Generated by Django 4.2.6 on 2023-10-11 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_ordinazione_piatto_ordinazione_piatto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordinazione',
            old_name='datadata_creazione',
            new_name='data_creazione',
        ),
    ]
