from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from vendor.models import Vendor
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestVendorAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate the client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('vendor.views.Vendor.objects.all')
    def test_get_all_vendors(self, mock_vendor_all):
        # Mocking the queryset
        mock_vendor_all.return_value = [
            Vendor(name='Vendor1', contact_details='Contact1', address='Address1', vendor_code='123'),
            Vendor(name='Vendor2', contact_details='Contact2', address='Address2', vendor_code='456')
        ]

        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['details']), 2)

    @patch('vendor.views.Vendor.objects.get')
    def test_get_single_vendor(self, mock_vendor_get):
        # Mocking the get method to return a single vendor
        mock_vendor_get.return_value = Vendor(name='Vendor1', contact_details='Contact1', address='Address1', vendor_code='123')

        response = self.client.get('/api/vendors/123/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['details']['name'], 'Vendor1')

    def test_create_vendor(self):
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': '789'
        }
        response = self.client.post('/api/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Vendor')

    @patch('vendor.views.Vendor.objects.get')
    def test_update_vendor(self, mock_vendor_get):
        # Mocking the get method to return a single vendor
        mock_vendor_get.return_value = Vendor(name='Vendor1', contact_details='Contact1', address='Address1', vendor_code='123')

        data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated Contact',
            'address': 'Updated Address',
            'vendor_code': '123'
        }
        response = self.client.put('/api/vendors/123/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Vendor')

    @patch('vendor.views.Vendor.objects.get')
    def test_delete_vendor(self, mock_vendor_get):
        # Mocking the get method to return a single vendor
        mock_vendor_get.return_value = Vendor(name='Vendor1', contact_details='Contact1', address='Address1', vendor_code='123')

        response = self.client.delete('/api/vendors/123/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['details'], 'Successfully deleted')


class TestVendorPerformanceAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and authenticate the client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    @patch('vendor.views.Vendor.objects.get')
    def test_get_vendor_performance(self, mock_vendor_get):
        # Mocking the get method to return a single vendor
        mock_vendor_get.return_value = Vendor(name='Vendor1', contact_details='Contact1', address='Address1', vendor_code='123', on_time_delivery_rate=95.5, quality_rating_avg=4.5, average_response_time=2.3, fulfillment_rate=98.7)

        response = self.client.get('/api/vendors/123/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('details', response.data)
        self.assertIsInstance(response.data['details'], dict)

        expected_data = {
            'name': 'Vendor1',
            'contact_details': 'Contact1',
            'address': 'Address1',
            'vendor_code': '123',
            'on_time_delivery_rate': 95.5,
            'quality_rating_avg': 4.5,
            'average_response_time': 2.3,
            'fulfillment_rate': 98.7
        }
        self.assertEqual(response.data['details'], expected_data)

    @patch('vendor.views.Vendor.objects.get')
    def test_get_vendor_performance_not_found(self, mock_vendor_get):
        # Mocking the get method to raise a Vendor.DoesNotExist exception
        mock_vendor_get.side_effect = Vendor.DoesNotExist

        response = self.client.get('/api/vendors/123/performance/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('details', response.data)
        self.assertEqual(response.data['details'], 'Vendor object does not exist.')

    @patch('vendor.views.Vendor.objects.get')
    def test_get_vendor_performance_error(self, mock_vendor_get):
        # Mocking the get method to raise an exception
        mock_vendor_get.side_effect = Exception('Some Error Occurred.')

        response = self.client.get('/api/vendors/123/performance/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)
        self.assertEqual(response.data['details'], 'Some Error Occurred.')
