from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class RegisterAPIViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")

    def test_register_user(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword",
            "password_repeat": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+38 000 000 00 00"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
