from django.db import migrations
from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='admin123#',
            email='admin@example.com'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'), # Update this with the latest migration
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]