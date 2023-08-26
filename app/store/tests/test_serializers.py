from django.test import TestCase
from store.serializers import BooksSerializer
from store.models import Book
from collections import OrderedDict


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, author='User1')
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00, author='User2')
        self.book_3 = Book.objects.create(name='The lord of the rings', price=900.00, author='User3')

    def test_ok(self):

        data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        expected_result = [
            {
                "id": self.book_1.id,
                "name": "Harry Potter",
                "price": "1000.00",
                'author': 'User1',
            },
            {
                "id": self.book_2.id,
                "name": "The Witcher",
                "price": "700.00",
                'author': 'User2',
            },
                        {
                "id": self.book_3.id,
                "name": "The lord of the rings",
                "price": "900.00",
                'author': 'User3',
            }
        ]
        self.assertEqual(expected_result, data)


