# Generated by Django 5.1.7 on 2025-03-15 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_rename_bank_branches_company_banks_branches_and_more'),
        ('master', '0011_remove_subcategory_company_code_subcategory_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='company_code',
        ),
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='company.company'),
        ),
    ]
