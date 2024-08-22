# Generated by Django 4.2.7 on 2024-08-22 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_salesmodel_sale_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesmodel',
            name='sale_currency',
            field=models.CharField(choices=[('AED', 'AED, United Arab Emirates Dirham'), ('ARS', 'ARS, Argentine Peso'), ('AUD', 'AUD, Australian Dollar'), ('BRL', 'BRL, Brazilian Real'), ('CAD', 'CAD, Canadian Dollar'), ('CHF', 'CHF, Swiss Franc'), ('CNY', 'CNY, Chinese Yuan'), ('COP', 'COP, Colombian Peso'), ('DKK', 'DKK, Danish Krone'), ('EUR', 'EUR, Euro'), ('GBP', 'GBP, British Pound Sterling'), ('HKD', 'HKD, Hong Kong Dollar'), ('ILS', 'ILS, Israeli New Shekel'), ('INR', 'INR, Indian Rupee'), ('JPY', 'JPY, Japanese Yen'), ('KRW', 'KRW, South Korean Won'), ('MXN', 'MXN, Mexican Peso'), ('MYR', 'MYR, Malaysian Ringgit'), ('NOK', 'NOK, Norwegian Krone'), ('NZD', 'NZD, New Zealand Dollar'), ('PLN', 'PLN, Polish Zloty'), ('RUB', 'RUB, Russian Ruble'), ('SAR', 'SAR, Saudi Riyal'), ('SEK', 'SEK, Swedish Krona'), ('SGD', 'SGD, Singapore Dollar'), ('THB', 'THB, Thai Baht'), ('TRY', 'TRY, Turkish Lira'), ('TWD', 'TWD, New Taiwan Dollar'), ('USD', 'USD, United States Dollar'), ('ZAR', 'ZAR, South African Rand'), ('ZWD', 'ZWD, Zimbabwe Dollar')], default='USD', max_length=4, verbose_name='currency'),
        ),
    ]