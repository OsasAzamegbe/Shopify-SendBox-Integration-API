from rest_framework.test import APITestCase
from django.urls import reverse
import requests
import random
import json


class TestMyAPI(APITestCase):

    def test_shipping_rates(self):
        body = {
            "rate": {
                "origin": {
                "country": "Nigeria",
                "postal_code": "K2P1L4",
                "province": "LA",
                "city": "Yaba",
                "name": None,
                "address1": "150 Elgin St.",
                "address2": "",
                "address3": None,
                "phone": "16135551212",
                "fax": None,
                "email": None,
                "address_type": None,
                "company_name": "Jamie D's Emporium"
                },
                "destination": {
                "country": "Nigeria",
                "postal_code": "K1M1M4",
                "province": "Abuja",
                "city": "Kuje",
                "name": "Bob Norman",
                "address1": "24 Sussex Dr.",
                "address2": "",
                "address3": None,
                "phone": None,
                "fax": None,
                "email": None,
                "address_type": None,
                "company_name": None
                },
                "items": [{
                "name": "Short Sleeve T-Shirt",
                "sku": "",
                "quantity": 1,
                "grams": 1000,
                "price": 1999,
                "vendor": "Jamie D's Emporium",
                "requires_shipping": True,
                "taxable": True,
                "fulfillment_service": "manual",
                "properties": None,
                "product_id": 48447225880,
                "variant_id": 258644705304
                },
                {
                "name": "Long Sleeve T-Shirt",
                "sku": "",
                "quantity": 1,
                "grams": 4000,
                "price": 1999,
                "vendor": "Jamie D's Emporium",
                "requires_shipping": True,
                "taxable": True,
                "fulfillment_service": "manual",
                "properties": None,
                "product_id": 48447200880,
                "variant_id": 258644005304
                }],
                "currency": "USD",
                "locale": "en"
            }
        }
        response = self.client.post(reverse('ShippingRates'), body, format='json')

        self.assertEqual(201, response.status_code)
        self.assertGreaterEqual(len(response.data), 1)
        for item in response.data['rates']:            
            self.assertIn("service_name", item)
            self.assertIn("service_code", item)
            self.assertIn("total_price", item)
            self.assertIn("description", item)
            self.assertIn("currency", item)
            self.assertIsNotNone(item["service_name"])
            self.assertIsNotNone(item["service_code"])
            self.assertIsNotNone(item["total_price"])
            self.assertIsNotNone(item["description"])
            self.assertIsNotNone(item["currency"])

    def test_shipping_rates_incomplete_info(self):
        body = {
            "rate": {
                "origin": {
                "country": "Nigeria",
                "postal_code": "K2P1L4",
                "province": "LA",
                "city": "Yaba",
                "name": None,
                "address1": "150 Elgin St.",
                "address2": "",
                "address3": None,
                "phone": "16135551212",
                "fax": None,
                "email": None,
                "address_type": None,
                "company_name": "Jamie D's Emporium"
                },
                "destination": {
                "country": "Ghana",
                "postal_code": "K1M1M4",
                "province": None,
                "city": "Accra",
                "name": "Bob Norman",
                "address1": "24 Sussex Dr.",
                "address2": "",
                "address3": None,
                "phone": None,
                "fax": None,
                "email": None,
                "address_type": None,
                "company_name": None
                },
                "items": [{
                "name": "Short Sleeve T-Shirt",
                "sku": "",
                "quantity": 1,
                "grams": 1000,
                "price": 1999,
                "vendor": "Jamie D's Emporium",
                "requires_shipping": True,
                "taxable": True,
                "fulfillment_service": "manual",
                "properties": None,
                "product_id": 48447225880,
                "variant_id": 258644705304
                },
                {
                "name": "Long Sleeve T-Shirt",
                "sku": "",
                "quantity": 1,
                "grams": 4000,
                "price": 1999,
                "vendor": "Jamie D's Emporium",
                "requires_shipping": True,
                "taxable": True,
                "fulfillment_service": "manual",
                "properties": None,
                "product_id": 48447200880,
                "variant_id": 258644005304
                }],
                "currency": "USD",
                "locale": "en"
            }
        }
        response = self.client.post(reverse('ShippingRates'), body, format='json')

        self.assertEqual(201, response.status_code)
        self.assertGreaterEqual(len(response.data), 1)
        for item in response.data['rates']:            
            self.assertIn("service_name", item)
            self.assertIn("service_code", item)
            self.assertIn("total_price", item)
            self.assertIn("description", item)
            self.assertIn("currency", item)
            self.assertIsNotNone(item["service_name"])
            self.assertIsNotNone(item["service_code"])
            self.assertIsNotNone(item["total_price"])
            self.assertIsNotNone(item["description"])
            self.assertIsNotNone(item["currency"])
            



