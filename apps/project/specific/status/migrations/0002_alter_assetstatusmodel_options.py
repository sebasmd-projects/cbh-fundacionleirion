# Generated by Django 4.2.7 on 2024-08-31 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assetstatusmodel',
            options={'ordering': ['default_order', '-created', 'buyer'], 'verbose_name': 'Assets Status', 'verbose_name_plural': 'Assets Statuses'},
        ),
    ]
