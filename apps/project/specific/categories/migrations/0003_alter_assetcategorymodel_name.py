# Generated by Django 4.2.7 on 2024-08-23 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_assetcategorymodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetcategorymodel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='category'),
        ),
    ]
