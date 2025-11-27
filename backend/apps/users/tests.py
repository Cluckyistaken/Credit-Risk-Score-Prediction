from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        u = User.objects.create_user(username="testuser", password="pass123")
        self.assertEqual(str(u), "testuser")
