from unittest import TestCase
from project_template.project_name_project import settings

class TestTransactionMiddleWare(TestCase):
    def test_transaction_middleware_exist(self):
        """
        TransactionMiddleware should be included by default

        We should use transaction middleware by default to avoid dealing
        with transaction problem later on when a project needs it.
        """
        print settings.MIDDLEWARE_CLASSES
        print settings.ROOT_URLCONF
        self.assertTrue('django.middleware.transaction.TransactionMiddleware' in
                      settings.MIDDLEWARE_CLASSES)
        
