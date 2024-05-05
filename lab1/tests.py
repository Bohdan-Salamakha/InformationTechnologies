from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Document

User = get_user_model()


class DocumentViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.document = Document.objects.create(
            name="Test Document",
            doc_type=Document.DocumentType.VACATION_REQUEST,
            body="Test Body",
            user=self.user
        )

    def test_list_documents(self):
        url = reverse('lab1:document-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_document_not_allowed(self):
        url = reverse('lab1:document-detail', kwargs={'pk': self.document.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_document(self):
        url = reverse('lab1:document-list')
        data = {
            'name': 'New Document',
            'doc_type': Document.DocumentType.EMPLOYMENT_APPLICATION,
            'body': 'New Body'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)

    def test_update_document_permission(self):
        url = reverse('lab1:document-detail', kwargs={'pk': self.document.pk})
        data = {'name': 'Updated Name'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(self.document.name, 'Updated Name')

    def test_delete_document_permission(self):
        url = reverse('lab1:document-detail', kwargs={'pk': self.document.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Document.objects.count(), 0)

    def tearDown(self):
        self.user.delete()
        Document.objects.all().delete()
