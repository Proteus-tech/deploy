from project_template.project_name_project import settings
from unittest import TestCase

class TestTransactionMiddleWare(TestCase):
    def test_transaction_middleware_exist(self):
        """
        TransactionMiddleware should be included by default

        We should use transaction middleware by default to avoid dealing
        with transaction problem later on when a project needs it.
        """
        self.assertTrue('django.middleware.transaction.TransactionMiddleware' in
                        settings.MIDDLEWARE_CLASSES)
        
