from django.test import TestCase
from .models import ModelRun

class ModelRunTest(TestCase):
    def test_model_run_create(self):
        r = ModelRun.objects.create(payload={"a": 1}, result={"r": 0.5})
        self.assertIsNotNone(r.id)
