import json
import tempfile

from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image

from accounts.models import UserProfile


"""class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "apitest", "email": "apitest@test.com", "first_name": "api",
                "last_name": "test", "password": "some_psw", "confirm_password": "some_psw"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse('password' in response.data)"""


class PermissionsTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "apitest", "email": "apitest@test.com", "first_name": "api",
                "last_name": "test", "password": "some_psw", "confirm_password": "some_psw"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.token = response.data["token"]
        self.assertFalse('password' in response.data)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    # def test_login(self):
    #     response = self.client.post(reverse('login'), {"email": "apitest@test.com",
    #                                                    "password": "some_psw"})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])

    def test_booklist_creation(self):
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        data = {"image": tmp_file, "name": "Apitest booklist"}
        response = self.client.post(reverse('booklist-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
