# Generated by Django 4.2.7 on 2024-09-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatemodel',
            name='document_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='Document number'),
        ),
        migrations.AlterField(
            model_name='certificatemodel',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]
