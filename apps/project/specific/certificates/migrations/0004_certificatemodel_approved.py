# Generated by Django 4.2.7 on 2024-10-21 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0003_certificatemodel_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatemodel',
            name='approved',
            field=models.BooleanField(default=True, verbose_name='Approved'),
        ),
    ]
