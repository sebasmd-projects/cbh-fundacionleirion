# Generated by Django 4.2.7 on 2024-08-22 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_salesmodel_amount_sold_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesmodel',
            name='buyer_country',
            field=models.CharField(default='US', max_length=50, verbose_name='country code'),
        ),
    ]