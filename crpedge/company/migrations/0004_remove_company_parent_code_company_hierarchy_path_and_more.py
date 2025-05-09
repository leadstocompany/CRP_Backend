# Generated by Django 5.1.7 on 2025-03-18 04:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_activesession_companyuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='parent_code',
        ),
        migrations.AddField(
            model_name='company',
            name='hierarchy_path',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='level',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='parent_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_companies', to='company.company'),
        ),
        migrations.AlterField(
            model_name='companyuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('member', 'Member'), ('staff', 'Staff'), ('manager', 'Manager')], default='member', max_length=10),
        ),
    ]
