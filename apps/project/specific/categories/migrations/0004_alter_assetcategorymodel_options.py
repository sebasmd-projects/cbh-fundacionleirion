# Generated by Django 4.2.7 on 2024-08-31 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_assetcategorymodel_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assetcategorymodel',
            options={'ordering': ['default_order', 'name', '-created'], 'verbose_name': 'Asset Category', 'verbose_name_plural': 'Assets Categories'},
        ),
    ]
