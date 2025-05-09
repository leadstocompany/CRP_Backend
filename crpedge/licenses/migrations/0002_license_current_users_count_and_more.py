# Generated by Django 5.1.7 on 2025-04-06 05:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_companyuser_otp_secret_key'),
        ('licenses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='current_users_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='license',
            name='max_users_allowed',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='license',
            name='company',
            field=models.ForeignKey(blank=True, help_text="Required if license_type is 'company'", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='company.company'),
        ),
        migrations.CreateModel(
            name='LicenseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='licenses.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'License Assignment',
                'verbose_name_plural': 'License Assignments',
                'unique_together': {('license', 'user')},
            },
        ),
    ]
