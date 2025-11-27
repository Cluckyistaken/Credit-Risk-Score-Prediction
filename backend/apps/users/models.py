from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Extends default Django user with a phone number and role to suit credit-risk project.
    """
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.email or str(self.id)
