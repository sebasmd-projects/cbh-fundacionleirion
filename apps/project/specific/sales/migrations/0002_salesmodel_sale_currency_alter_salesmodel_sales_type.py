# Generated by Django 4.2.7 on 2024-08-22 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesmodel',
            name='sale_currency',
            field=models.CharField(choices=[('AED', 'United Arab Emirates Dirham'), ('ARS', 'Argentine Peso'), ('AUD', 'Australian Dollar'), ('BRL', 'Brazilian Real'), ('CAD', 'Canadian Dollar'), ('CHF', 'Swiss Franc'), ('CNY', 'Chinese Yuan'), ('COP', 'Colombian Peso'), ('DKK', 'Danish Krone'), ('EUR', 'Euro'), ('GBP', 'British Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('ILS', 'Israeli New Shekel'), ('INR', 'Indian Rupee'), ('JPY', 'Japanese Yen'), ('KRW', 'South Korean Won'), ('MXN', 'Mexican Peso'), ('MYR', 'Malaysian Ringgit'), ('NOK', 'Norwegian Krone'), ('NZD', 'New Zealand Dollar'), ('PLN', 'Polish Zloty'), ('RUB', 'Russian Ruble'), ('SAR', 'Saudi Riyal'), ('SEK', 'Swedish Krona'), ('SGD', 'Singapore Dollar'), ('THB', 'Thai Baht'), ('TRY', 'Turkish Lira'), ('TWD', 'New Taiwan Dollar'), ('USD', 'United States Dollar'), ('ZAR', 'South African Rand'), ('ZWD', 'Zimbabwe Dollar')], default='USD', max_length=4, verbose_name='currency'),
        ),
        migrations.AlterField(
            model_name='salesmodel',
            name='sales_type',
            field=models.CharField(choices=[('DS', 'Direct Sales'), ('RD', 'RD'), ('O', 'Other')], default='DS', max_length=3, verbose_name='sales type'),
        ),
    ]