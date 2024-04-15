from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from payments.models import PaymentInfo

class PaymentInfoTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_add_payment_type(self):
        # Create a new payment type
        payment_info = PaymentInfo.objects.create(
            customer=self.user,
            cardholder='Test User',
            cardnumber='1234567890123456',
            expiration='2025-01-01',
            cvv=123,
            balance=100.00,
            is_default=True
        )

        # Check that the payment type was added successfully
        self.assertEqual(PaymentInfo.objects.count(), 1)
        self.assertEqual(payment_info.customer, self.user)
        self.assertEqual(payment_info.cardholder, 'Test User')
        self.assertEqual(payment_info.cardnumber, '1234567890123456')
        self.assertEqual(payment_info.expiration, '2025-01-01')
        self.assertEqual(payment_info.cvv, 123)
        self.assertEqual(payment_info.balance, 100.00)
        self.assertTrue(payment_info.is_default)

    def test_remove_payment_type(self):
        # Create a new payment type
        payment_info = PaymentInfo.objects.create(
            customer=self.user,
            cardholder='Test User',
            cardnumber='1234567890123456',
            expiration='2025-01-01',
            cvv=123,
            balance=100.00,
            is_default=True
        )

        # Remove the payment type
        payment_info.delete()

        # Check that the payment type was removed successfully
        self.assertEqual(PaymentInfo.objects.count(), 0)
