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
        data = {
            'name': 'Updated Name',
            'doc_type': Document.DocumentType.EMPLOYMENT_APPLICATION,
            'body': 'Updated body',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(self.document.name, 'Updated Name')
        self.assertEqual(self.document.body, 'Updated body')

    def test_delete_document_permission(self):
        url = reverse('lab1:document-detail', kwargs={'pk': self.document.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Document.objects.count(), 0)

    def test_filter_documents_signed(self):
        Document.objects.all().delete()
        Document.objects.create(
            name="Signed Document",
            doc_type=Document.DocumentType.VACATION_REQUEST,
            body="Signed Body",
            user=self.user,
            signature_date="2021-01-01"
        )
        Document.objects.create(
            name="Unsigned Document",
            doc_type=Document.DocumentType.VACATION_REQUEST,
            body="Unsigned Body",
            user=self.user
        )

        response = self.client.get(reverse('lab1:document-list'), {'is_signed': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Signed Document")

        response = self.client.get(reverse('lab1:document-list'), {'is_signed': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Unsigned Document")

    def test_filter_documents_by_date(self):
        response = self.client.get(
            reverse('lab1:document-list'),
            {'start_date': '2020-01-01', 'end_date': '2030-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_document_permission_denied(self):
        other_user = User.objects.create_user(username='other_user', password='67890')
        self.client.force_authenticate(user=other_user)
        url = reverse('lab1:document-detail', kwargs={'pk': self.document.pk})
        data = {'name': 'Unauthorized Update'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_document_permission_denied(self):
        other_user = User.objects.create_user(username='other_user', password='67890')
        self.client.force_authenticate(user=other_user)
        url = reverse('lab1:document-detail', kwargs={'pk': self.document.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_document_invalid_data(self):
        url = reverse('lab1:document-list')
        data = {
            'name': '',
            'doc_type': Document.DocumentType.EMPLOYMENT_APPLICATION,
            'body': 'Some Body'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        super().tearDown()
        Document.objects.all().delete()
        User.objects.all().delete()
