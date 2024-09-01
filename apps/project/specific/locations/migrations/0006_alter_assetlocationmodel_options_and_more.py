# Generated by Django 4.2.7 on 2024-08-31 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_assetlocationmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assetlocationmodel',
            options={'ordering': ['default_order', 'asset', '-created'], 'verbose_name': 'Assets Location', 'verbose_name_plural': 'Assets Locations'},
        ),
        migrations.AlterModelOptions(
            name='locationmodel',
            options={'ordering': ['default_order', 'reference', 'owner', '-created'], 'verbose_name': 'Location', 'verbose_name_plural': 'Locations'},
        ),
    ]