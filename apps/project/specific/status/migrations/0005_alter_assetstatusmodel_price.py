# Generated by Django 4.2.7 on 2024-09-01 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0004_remove_assetstatusmodel_total_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetstatusmodel',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=60, null=True, verbose_name='price'),
        ),
    ]
