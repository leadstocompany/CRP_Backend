# Generated by Django 5.1.7 on 2025-03-17 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0020_remove_currencycode_company_code_and_more'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportconfiguration',
            name='filters',
        ),
        migrations.RemoveField(
            model_name='reportconfiguration',
            name='modified_at',
        ),
        migrations.AddField(
            model_name='reportconfiguration',
            name='filter1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.filter1'),
        ),
        migrations.AddField(
            model_name='reportconfiguration',
            name='filter2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.filter2'),
        ),
        migrations.AddField(
            model_name='reportconfiguration',
            name='sub_filter1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.subfilter1'),
        ),
        migrations.AddField(
            model_name='reportconfiguration',
            name='sub_filter2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.subfilter2'),
        ),
        migrations.AlterField(
            model_name='reportconfiguration',
            name='report_name',
            field=models.CharField(max_length=100),
        ),
    ]
