from django.test import TestCase
from store.serializers import BooksSerializer
from store.models import Book
from collections import OrderedDict


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00)
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00)

    def test_ok(self):

        data = BooksSerializer([self.book_1, self.book_2], many=True).data
        expected_result = [
            {
                "id": self.book_1.id,
                "name": "Harry Potter",
                "price": "1000.00"
            },
            {
                "id": self.book_2.id,
                "name": "The Witcher",
                "price": "700.00"
            }
        ]
        self.assertEqual(expected_result, data)

