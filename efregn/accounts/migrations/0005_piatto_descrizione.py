# Generated by Django 4.2.6 on 2023-10-10 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_ordinazione_cliente_ordinazione_piatto'),
    ]

    operations = [
        migrations.AddField(
            model_name='piatto',
            name='descrizione',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
