# Generated by Django 4.2.7 on 2024-09-30 19:41

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateModel',
            fields=[
                ('language', models.CharField(blank=True, choices=[('es', 'Spanish'), ('en', 'English')], default='es', max_length=4, null=True, verbose_name='language')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('default_order', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='priority')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Certificate',
                'verbose_name_plural': 'Certificates',
                'db_table': 'apps_project_specific_certificates_certificate',
                'ordering': ['default_order', '-created'],
                'permissions': [('view_certificate', 'Can view certificate list')],
            },
        ),
    ]
