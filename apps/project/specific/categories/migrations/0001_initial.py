# Generated by Django 4.2.7 on 2024-08-22 08:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BondCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('es', 'Spanish'), ('en', 'English')], default='es', max_length=4, null=True, verbose_name='language')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('default_order', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='priority')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bondcategory_bondcategory', to='categories.bondcategorymodel', verbose_name='sub category')),
            ],
            options={
                'verbose_name': 'Bond Category',
                'verbose_name_plural': 'Bond Categories',
                'db_table': 'apps_project_specific_categories_bondcategory',
            },
        ),
    ]
