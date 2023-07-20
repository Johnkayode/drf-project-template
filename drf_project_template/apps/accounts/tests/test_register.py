from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_project_template.apps.accounts.models import User



class RegisterTest(APITestCase):
    def test_accounts(self):
        """
        Ensure user can create account, activate account and login
        """
        url = reverse("register")
        data = {
            "email": "johndoe@example.com",
            "password1": "johnxxx0101",
            "password2": "johnxxx0101",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "08003377118"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "johndoe@example.com")
        print("----Account Created Succesfully----")

        # test login user before activation
        url = reverse("user-login")
        data = {"email": "johndoe@example.com", "password": "johnxxx0101"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        print("----Unauthorized Login----")