# Generated by Django 4.2.7 on 2024-08-22 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverhttp', '0002_alter_iptoblockmodel_options_iptoblockmodel_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iptoblockmodel',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is blocked'),
        ),
    ]