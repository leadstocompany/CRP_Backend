from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from .models import License


def get_license_email(instance: License):
    """
    Helper function to get the associated email address for a license.
    Supports both company and individual license types.
    """
    if instance.license_type == 'individual' and instance.user:
        return instance.user.email
    elif instance.license_type == 'company' and instance.company:
        # Optional: if company has a contact_email field or a company admin user
        return instance.company.admin.email if hasattr(instance.company, 'admin') else None
    return None


@receiver(post_save, sender=License)
def send_license_created_email(sender, instance, created, **kwargs):
    """
    Send an email notification when a new license is created.
    """
    if created:
        user_email = get_license_email(instance)
        if user_email:
            send_mail(
                subject='✅ Your License Has Been Created',
                message=f'Your license ({instance.license_key}) is now active and valid until {instance.end_date}.',
                from_email='noreply@example.com',
                recipient_list=[user_email],
                fail_silently=False,
            )
            print(f'✅ License creation email sent to: {user_email}')


@receiver(post_save, sender=License)
def send_license_expiry_reminder(sender, instance, **kwargs):
    """
    Send a reminder email if a license is about to expire within 7 days.
    """
    if instance.end_date and instance.status == 'active':
        days_remaining = (instance.end_date - timezone.now().date()).days
        if 0 < days_remaining <= 7:
            user_email = get_license_email(instance)
            if user_email:
                send_mail(
                    subject='⚠️ License Expiry Reminder',
                    message=(
                        f'Your license ({instance.license_key}) will expire in {days_remaining} day(s) on {instance.end_date}. '
                        'Please renew it to avoid service interruption.'
                    ),
                    from_email='noreply@example.com',
                    recipient_list=[user_email],
                    fail_silently=False,
                )
                print(f'⚠️ Expiry reminder sent to: {user_email}')
