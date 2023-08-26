from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer

class BooksApiTestCase(APITestCase):

    def test_get(self):
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00)
        self.book_2 = Book.objects.create(name='The Wichter', price=700.00)

        # url = reverse('book-list')
        url = '/book/'  # 'http://127.0.0.1:8000/book/'
        response = self.client.get(url)
        serializer_data  = BooksSerializer([self.book_1, self.book_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


        print(response.data)