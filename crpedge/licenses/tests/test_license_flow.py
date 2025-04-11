
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from licenses.models import Customer, License
from licenses.utils import generate_license_key
from datetime import timedelta
from django.test import override_settings

User = get_user_model()
@override_settings(LICENSE_ENFORCEMENT=False)  # if such a setting exists
class LicenseFlowTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.customer = Customer.objects.create(user=self.user)
        self.client.login(username='testuser', password='pass1234')

    def test_trial_license_creation(self):
        response = self.client.post('/api/license/trial/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(License.objects.filter(customer=self.customer, is_trial=True).exists())

    def test_prevent_second_trial(self):
        # Create first trial
        self.client.post('/api/license/trial/')
        # Try creating second one
        response = self.client.post('/api/license/trial/')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Trial already used", response.data['error'])

    def test_paid_license_creation_directly(self):
        from licenses.services import SubscriptionService
        service = SubscriptionService(self.customer)

        paid_license = service.generate_paid_license(self.customer)
        self.assertEqual(paid_license.is_trial, False)
        self.assertEqual(paid_license.status, 'active')
        self.assertTrue(len(paid_license.license_key) == 12)
    def test_license_renewal(self):
        # First create a paid license manually
        from licenses.services import SubscriptionService
        service = SubscriptionService(self.customer)
        paid_license = service.generate_paid_license(self.customer)

        # Renew via API
        response = self.client.post('/api/license/renew/')
        self.assertEqual(response.status_code, 200)
        updated_license = License.objects.get(id=paid_license.id)

        self.assertGreater(updated_license.end_date, paid_license.end_date - timedelta(days=365))
        self.assertNotEqual(updated_license.license_key, paid_license.license_key)
