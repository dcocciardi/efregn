# Generated by Django 4.2.6 on 2023-10-11 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_piatto_immagine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piatto',
            name='immagine',
            field=models.ImageField(blank=True, null=True, upload_to='piatti/'),
        ),
    ]