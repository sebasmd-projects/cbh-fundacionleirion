# Generated by Django 4.2.7 on 2024-08-22 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bondmodel',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]