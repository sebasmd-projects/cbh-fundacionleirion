# Generated by Django 4.2.7 on 2024-08-22 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverhttp', '0003_alter_iptoblockmodel_is_active'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IPToBlockModel',
            new_name='IPBlockedModel',
        ),
    ]