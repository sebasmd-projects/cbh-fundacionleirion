# Generated by Django 4.2.7 on 2024-09-01 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_assetstatusmodel_total_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetstatusmodel',
            name='total_quantity',
        ),
    ]
