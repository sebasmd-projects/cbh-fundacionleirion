# Generated by Django 4.2.7 on 2024-08-29 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_alter_assetstatusreferencemodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assetstatusreferencemodel',
            options={'verbose_name': 'Assets Status Reference', 'verbose_name_plural': 'Assets Statuses References'},
        ),
        migrations.AlterUniqueTogether(
            name='assetlocationmodel',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='assetmodel',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='assetstatusreferencemodel',
            name='asset_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assetstatus_references', to='assets.assetstatusmodel', verbose_name='asset status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assetstatusreferencemodel',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assetstatusreference_location', to='assets.assetlocationmodel', verbose_name='supplier'),
        ),
    ]