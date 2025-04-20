from django.test import TestCase
from accounts.models import CustomUser
from rest_framework import serializers


class CustomUserModelTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            phone="+38 000 000 00 00"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone, "+38 000 000 00 00")

    def test_str_method(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            phone="+38 000 000 00 00"
        )
        self.assertEqual(str(user), "test@example.com")

    def test_phone_validation(self):
        with self.assertRaises(serializers.ValidationError):
            CustomUser.objects.create_user(
                email="invalid@example.com",
                username="invaliduser",
                password="testpassword",
                first_name="Invalid",
                last_name="User",
                phone="invalid_phone"
            )
