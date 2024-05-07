from django.test import TestCase
from purchase.views import PurchaseOrderAPIView, PurchaseOrderAcknowledgeAPIView
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from unittest.mock import Mock, patch
from purchase.models import PurchaseOrder
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from vendor.models import Vendor
from django_mock_queries.query import MockSet, MockModel

class TestPurchaseOrderAPIView(TestCase):
    view = PurchaseOrderAPIView
    
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate the client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='1234567890', address='Test Address', vendor_code='123')

    @patch('purchase.views.PurchaseOrder.objects.get')
    def test_get_purchase_order(self, mock_purchaseorder_get):
        # Create a PurchaseOrder for testing
        # purchase_order = PurchaseOrder(po_number='PO123', vendor=Vendor(), order_date=timezone.now(), delivery_date=timezone.now() + timedelta(days=7), items={}, quantity=10, status='pending', issue_date=timezone.now())
        mock_purchaseorder_get.return_value = PurchaseOrder(po_number='PO123', vendor=Vendor(), order_date=timezone.now(), delivery_date=timezone.now() + timedelta(days=7), items={}, quantity=10, status='pending', issue_date=timezone.now())
        response = self.client.get('/api/purchase_orders/PO123/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('details', response.data)
        self.assertIsInstance(response.data['details'], dict)

    def test_get_purchase_orders_list(self):
        # Create some PurchaseOrders for testing
        PurchaseOrder.objects.create(po_number='PO1', vendor=Vendor.objects.create(), order_date=timezone.now(), delivery_date=timezone.now() + timedelta(days=7), items={}, quantity=10, status='pending', issue_date=timezone.now())
        PurchaseOrder.objects.create(po_number='PO2', vendor=Vendor.objects.create(), order_date=timezone.now(), delivery_date=timezone.now() + timedelta(days=7), items={}, quantity=10, status='pending', issue_date=timezone.now())

        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('details', response.data)
        self.assertIsInstance(response.data['details'], list)

    def test_post_purchase_order(self):
        # Test POST request to create a new purchase order
        data = {
            'po_number': 'PO123',
            'vendor': '123',
            'order_date': '2024-05-15',
            'delivery_date': '2024-05-20',
            'items': {},
            'quantity': 10,
            'status': 'pending',
            'issue_date': '2024-05-20'
        }
        response = self.client.post('/api/purchase_orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO123')

    @patch('purchase.views.PurchaseOrder.objects.get')
    def test_put_purchase_order(self, mock_purchaseorder_get):
        # Create a purchase order for testing
        # purchase_order = PurchaseOrder.objects.create(po_number='PO123', vendor=Vendor.objects.create(), order_date='2024-05-15', delivery_date='2024-05-20', items={}, quantity=10, status='pending', issue_date=timezone.now())

        # Test PUT request to update an existing purchase order
        data = {
            'vendor': '123',
            'status': 'updated',
            'delivery_date': '2024-05-10',
            'items': {},
            'quantity': 10,
            'status': 'completed',
            'issue_date': '2024-05-10',
        }
        mock_purchaseorder_get.return_value = PurchaseOrder(po_number='PO123', vendor=Vendor(), order_date=timezone.now(), delivery_date=timezone.now() + timedelta(days=7), items={}, quantity=10, status='pending', issue_date=timezone.now())
        response = self.client.put('/api/purchase_orders/PO123/', data, format='json')
        # response = self.view(request, po_id='PO123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vendor'], '123')
        self.assertEqual(response.data['status'], 'completed')

class PurchaseOrderAcknowledgeAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PurchaseOrderAcknowledgeAPIView.as_view()
        self.vendor = Vendor.objects.create(name="Test Vendor")
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO-001",
            issue_date=timezone.now() - timedelta(days=1),
            vendor=self.vendor,
            delivery_date=timezone.now(),
            items={},
            quantity=10,
        )

    def test_already_acknowledged_purchase_order(self):
        self.purchase_order.acknowledgment_date = timezone.now()
        self.purchase_order.save()

        url = f"/purchase-orders/{self.purchase_order.po_number}/acknowledge/"
        request = self.factory.post(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, po_id=self.purchase_order.po_number)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],
            "This purchase order has already been acknowledged."
        )

    def test_nonexistent_purchase_order(self):
        url = "/purchase-orders/invalid-po-number/acknowledge/"
        request = self.factory.post(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, po_id="invalid-po-number")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["details"],
            "Purchase Order object does not exist."
        )

    def test_generic_exception_handling(self):
        # Simulate an unexpected exception during processing
        url = f"/purchase-orders/{self.purchase_order.po_number}/acknowledge/"
        request = self.factory.post(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, po_id=self.purchase_order.po_number)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["details"],
            "Some Error Occurred."
        )
