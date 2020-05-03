import json

from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from .models import UserProfile




class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app", "first_name": "test",
                "last_name": "case", "password": "some_psw", "confirm_password": "some_psw"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse('password' in response.data)

class GeneralUserProfileTestCase(APITestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_users(email="freud@test.com",
                                            username="freudie",
                                            first_name="freud1",
                                            last_name="freud2",
                                            password="notailigot")
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.api_authentication()
    
    def test_login(self):
        response = self.client.post(reverse('login'), {"email":"freud@test.com", 
                                                        "password": "notailigot"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_userlist_authenticated(self):
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_userlist_unauthenticated(self):
    #     response = self.client.get(reverse('users-list'))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userdetail_retrieve(self):
        response = self.client.get(reverse("users-detail", kwargs={"username": "freudie"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "freudie")

    def test_userdetail_update_by_owner(self):
        response = self.client.put(reverse("users-detail", kwargs={"username": "freudie"}),
                                   {"first_name": "freud1updated", "last_name": "freud2updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"id":1, "email": "freud@test.com",
                                                        "username":"freudie", 
                                                        "first_name": "freud1updated", 
                                                        "last_name": "freud2updated"})

    def test_userdetail_update_by_random_user(self):
        random_user = UserProfile.objects.create_users(email="random@test.com",
                                            username="random_user",
                                            first_name="random",
                                            last_name="random",
                                            password="somerandompassword")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("users-detail", kwargs={"username": "freudie"}),
                                   {"first_name": "foooool!!", "last_name": "foooool!!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # Additionally, we want to return the username and email upon successful creation.
#         self.assertEqual(response.data['username'], data['username'])
#         self.assertEqual(response.data['email'], data['email'])
#         self.assertFalse('password' in response.data)

# def