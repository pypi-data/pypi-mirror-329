from django.apps import apps
from django.test import TestCase


class ContractsTestCase(TestCase):
    def test_contracts_app_is_installed(self):
        assert apps.is_installed("NEMO_contracts")
