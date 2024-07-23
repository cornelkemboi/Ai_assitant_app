# api/tests.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Document
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'}

    def test_register_user(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user(self):
        self.client.post(reverse('register'), self.user_data)
        response = self.client.post(reverse('login'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Check for DRF token in response


class DocumentTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.upload_url = reverse('upload')
        self.document_data = {
            'original_file': SimpleUploadedFile('test.txt', b'This is a test document.')
        }

    def test_upload_document(self):
        response = self.client.post(self.upload_url, self.document_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)

    # def test_get_document_detail(self):
    #     document = Document.objects.create(user=self.user,
    #                                        original_file=SimpleUploadedFile('test.txt', b'This is a test document.'))
    #     detail_url = reverse('document_detail', kwargs={'pk': document.id})
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.get(detail_url)
    #     print(response.status_code)  # Debug statement
    #     print(response.data)  # Debug statement
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('original_file', response.data)
