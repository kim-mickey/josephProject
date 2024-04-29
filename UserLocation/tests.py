# tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
import json

from .models import CountryWhitelist
from .views import index, error_view

class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.whitelisted_country = CountryWhitelist.objects.create(country_name='United States')
        self.non_whitelisted_country = 'Canada'

    @patch('views.requests.get')
    def test_successful_access(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps({'country': 'United States'})

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('views.requests.get')
    def test_access_denied(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps({'country': 'Canada'})

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))

        self.assertRedirects(response, reverse('error_view'))

    @patch('views.requests.get')
    def test_ip_geolocation_api_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = 'Invalid response'

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))

        # Add appropriate assertions based on your error handling or fallback mechanism

    def test_authentication_required(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertRedirects(response, f"/accounts/login/?next={reverse('index')}")

    def test_country_whitelist_model(self):
        country = CountryWhitelist.objects.create(country_name='Germany')
        self.assertEqual(country.country_name, 'Germany')

        country.country_name = 'France'
        country.save()
        self.assertEqual(country.country_name, 'France')

        country.delete()
        self.assertFalse(CountryWhitelist.objects.filter(country_name='France').exists())

    def test_error_view(self):
        response = self.client.get(reverse('error_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')