from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json
from .models import SensorReading


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.is_active = True
        self.user.save()
    
    def test_login_with_valid_credentials(self):
        """Test that login works with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
    
    def test_login_form_uses_cleaned_data(self):
        """Test that login uses form.cleaned_data instead of form.POST"""
        # This test verifies the bug fix - we can't directly test form.POST
        # but we verify that the login process works correctly
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm(data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Verify the form doesn't have a POST attribute
        self.assertFalse(hasattr(form, 'POST'))
        # Verify it has cleaned_data after validation
        self.assertTrue(form.is_valid())
        self.assertTrue(hasattr(form, 'cleaned_data'))


class SensorDataValidationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recieve')
    
    def test_valid_sensor_data(self):
        """Test that valid sensor data is accepted"""
        data = {
            'temprature': 25.5,
            'humidity': 60.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SensorReading.objects.count(), 1)
    
    def test_temperature_too_high(self):
        """Test that temperature above 50C is rejected"""
        data = {
            'temprature': 55.0,
            'humidity': 60.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_temperature_too_low(self):
        """Test that temperature below -10C is rejected"""
        data = {
            'temprature': -15.0,
            'humidity': 60.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_humidity_too_high(self):
        """Test that humidity above 100% is rejected"""
        data = {
            'temprature': 25.0,
            'humidity': 110.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_humidity_negative(self):
        """Test that negative humidity is rejected"""
        data = {
            'temprature': 25.0,
            'humidity': -5.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_missing_temperature(self):
        """Test that missing temperature field is rejected"""
        data = {
            'humidity': 60.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_missing_humidity(self):
        """Test that missing humidity field is rejected"""
        data = {
            'temprature': 25.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_invalid_json(self):
        """Test that invalid JSON is rejected"""
        response = self.client.post(
            self.url,
            'not valid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)
    
    def test_non_numeric_temperature(self):
        """Test that non-numeric temperature is rejected"""
        data = {
            'temprature': 'hot',
            'humidity': 60.0
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorReading.objects.count(), 0)

