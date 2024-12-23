# Generated by Django 4.2.7 on 2024-10-28 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0004_certificatemodel_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatemodel',
            name='document_type',
            field=models.CharField(choices=[('CC', 'Citizen ID'), ('CE', 'Foreigner ID'), ('PPT', 'Special Residence Permit'), ('TI', 'Identity Card'), ('PA', 'Passport'), ('RC', 'Civil Registry'), ('NIT', 'Tax Identification Number'), ('RUT', 'Single Tax Registry'), ('CD', 'Diplomatic ID Card')], default='CC', max_length=4, verbose_name='Document type'),
        ),
        migrations.AlterField(
            model_name='certificatemodel',
            name='document_number',
            field=models.CharField(max_length=20, verbose_name='Document number'),
        ),
        migrations.AlterUniqueTogether(
            name='certificatemodel',
            unique_together={('document_number', 'document_type')},
        ),
    ]
