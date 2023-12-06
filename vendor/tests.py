from django.test import TestCase

# Create your tests here.
# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder
from django.urls import reverse
import json
from datetime import datetime, timedelta

class VendorManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_vendor(self):
        data = {
                'name': 'Vendor 1',
                'contact_details': 'Contact details',
                'address': 'Vendor address',
                'vendor_code': 'V123'
               }
        response = self.client.post(reverse('vendor-list-create'), data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Vendor 1')

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(name='Vendor 2', 
                                       contact_details='Contact details', 
                                       address='Vendor address', 
                                       vendor_code='V124')

        response = self.client.get(reverse('vendor-retrieve-update-delete', args=[vendor.id]))
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor 2')

    def test_acknowledge_purchase_order(self):
        vendor = Vendor.objects.create(
            name='Vendor 3',
            contact_details='Contact details',
            address='Vendor address',
            vendor_code='V125',
            on_time_delivery_rate=0.0,  # Provide a default value
            quality_rating_avg=0.0,  # Provide a default value
            average_response_time=0.0,  # Provide a default value
            fulfillment_rate=0.0  # Provide a default value
        )

        po_data = {
            'po_number': 'PO123',
            'vendor': vendor.id,
            'order_date': datetime.now().isoformat(),
            'delivery_date': (datetime.now() + timedelta(days=7)).isoformat(),
            "items": {
                        "items": {
                            "item1": "1",
                            "item2": "2"
                        }
                     },
            'quantity': 15,
            'status': 'pending',
            'issue_date': datetime.now().isoformat()
        }
        response = self.client.post(reverse('purchase-order-list-create'), po_data, format='json')
        print(response.content)
        po_id = response.data['id']

        ack_response = self.client.post(reverse('acknowledge-purchase-order', args=[po_id]))
        self.assertEqual(ack_response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(PurchaseOrder.objects.get(pk=po_id).acknowledgment_date)

    def test_vendor_performance(self):
        vendor = Vendor.objects.create(name='Vendor 4', 
                                       contact_details='Contact details', 
                                       address='Vendor address', 
                                       vendor_code='V126')

        response = self.client.get(reverse('vendor-performance', args=[vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)
