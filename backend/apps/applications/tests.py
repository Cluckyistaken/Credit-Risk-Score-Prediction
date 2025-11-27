from django.test import TestCase
from .models import CreditApplication

class CreditApplicationTest(TestCase):
    def test_create_application(self):
        app = CreditApplication.objects.create(
            name="Test Applicant",
            requested_amount=10000,
        )
        self.assertEqual(app.name, "Test Applicant")
