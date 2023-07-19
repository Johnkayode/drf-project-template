from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase



class RegisterTest(APITestCase):
    def test_accounts(self):
        """
        Ensure user can create account, activate account and login
        """
        url = reverse("register")
        data = {
            "email": "user@example.com",
            "password1": "johnxxx0101",
            "password2": "johnxxx0101",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "08003377118"
        }
        response = self.client.post(url, data, format="json")