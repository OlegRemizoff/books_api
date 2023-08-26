from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer

class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, author='J. K. Rowling')
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00, author='Andrzej Sapkowski')
        self.book_3 = Book.objects.create(name='The lord of the Rowling', price=900.00, author='Tolkien')

    def test_get(self):
        # url = reverse('book-list')
        url = '/book/'  # 'http://127.0.0.1:8000/book/'
        response = self.client.get(url)
        serializer_data  = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Rowling'})
        serializer_data  = BooksSerializer([self.book_1, self.book_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)



    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data  = BooksSerializer([self.book_2, self.book_3, self.book_1], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
