from django.test import TestCase
from accounts.serializers import RegisterSerializer


class RegisterSerializerTest(TestCase):

    def test_valid_data(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword",
            "password_repeat": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+38 000 000 00 00"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            "email": "invalid_email",
            "username": "invaliduser",
            "password": "testpassword",
            "password_repeat": "testpassword",
            "first_name": "Invalid",
            "last_name": "User",
            "phone": "invalid_phone"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
