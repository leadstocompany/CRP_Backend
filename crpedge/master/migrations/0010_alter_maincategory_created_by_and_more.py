# Generated by Django 5.1.7 on 2025-03-15 04:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0009_remove_maincategory_company_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='maincategory',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='maincategory',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_modified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
