# Generated by Django 4.2.7 on 2024-08-24 05:17

import apps.project.specific.assets.signals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_alter_assetmodel_observations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmodel',
            name='asset_img',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=apps.project.specific.assets.signals.assets_directory_path, verbose_name='img'),
        ),
    ]
