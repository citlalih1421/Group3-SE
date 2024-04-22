from django.test import TestCase
from django.contrib.auth import get_user_model
from store.models import Shoe
from orders.models import ShippingInfo, OrderItem, Order
from django.utils import timezone

User = get_user_model()

class ShippingInfoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_add_shipping_info(self):
        shipping_info = ShippingInfo.objects.create(
            customer=self.user,
            street='123 Test St',
            city='Test City',
            zipcode=12345,
            state='Test State',
            country='Test Country',
            is_default=True
        )
        self.assertEqual(ShippingInfo.objects.count(), 1)
        self.assertEqual(shipping_info.customer, self.user)
        self.assertEqual(shipping_info.street, '123 Test St')
        self.assertEqual(shipping_info.city, 'Test City')
        self.assertEqual(shipping_info.zipcode, 12345)
        self.assertEqual(shipping_info.state, 'Test State')
        self.assertEqual(shipping_info.country, 'Test Country')
        self.assertTrue(shipping_info.is_default)

    def test_remove_shipping_info(self):
        shipping_info = ShippingInfo.objects.create(
            customer=self.user,
            street='123 Test St',
            city='Test City',
            zipcode=12345,
            state='Test State',
            country='Test Country',
            is_default=True
        )
        shipping_info.delete()
        self.assertEqual(ShippingInfo.objects.count(), 0)

class OrderItemTests(TestCase):
    def setUp(self):
        self.shoe = Shoe.objects.create(name='Test Shoe', price=100.00)

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(shoe=self.shoe, quantity=2, total=200.00)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(order_item.shoe, self.shoe)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.total, 200.00)

class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.shipping_info = ShippingInfo.objects.create(
            customer=self.user,
            street='123 Test St',
            city='Test City',
            zipcode=12345,
            state='Test State',
            country='Test Country',
            is_default=True
        )
        self.shoe = Shoe.objects.create(name='Test Shoe', price=100.00)
        self.order_item = OrderItem.objects.create(shoe=self.shoe, quantity=2, total=200.00)

    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.user,
            shippinginfo=self.shipping_info,
            quantity=2,
            total=200.00,
            is_refunded=False,
            date_ordered=timezone.now()
        )
        order.items.add(self.order_item)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.shippinginfo, self.shipping_info)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total, 200.00)
        self.assertFalse(order.is_refunded)
        self.assertIn(self.order_item, order.items.all())
        self.assertIsNotNone(order.date_ordered)

    def test_order_refund(self):
        order = Order.objects.create(
            customer=self.user,
            shippinginfo=self.shipping_info,
            quantity=2,
            total=200.00,
            is_refunded=False,
            date_ordered=timezone.now()
        )
        order.items.add(self.order_item)

        # Refund the order
        order.is_refunded = True
        order.save()

        # Check that the order is marked as refunded
        self.assertTrue(order.is_refunded)

    def test_order_item_string_representation(self):
        order_item = OrderItem.objects.create(shoe=self.shoe, quantity=2, total=200.00)
        self.assertEqual(str(order_item), str(order_item.id))

    def test_shipping_info_string_representation(self):
        shipping_info = ShippingInfo.objects.create(
            customer=self.user,
            street='123 Test St',
            city='Test City',
            zipcode=12345,
            state='Test State',
            country='Test Country',
            is_default=True
        )
        self.assertEqual(str(shipping_info), f"{shipping_info.street}, {shipping_info.city}, {shipping_info.country}")

    def test_order_string_representation(self):
        order = Order.objects.create(
            customer=self.user,
            shippinginfo=self.shipping_info,
            quantity=2,
            total=200.00,
            is_refunded=False,
            date_ordered=timezone.now()
        )
        order.items.add(self.order_item)
        self.assertEqual(str(order), str(order.id))
