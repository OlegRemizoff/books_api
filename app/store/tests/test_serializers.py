from django.test import TestCase
from django.contrib.auth.models import User
from store.serializers import BooksSerializer
from store.models import Book
from collections import OrderedDict


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, 
                                          author='User1', owner=self.user)
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00,
                                          author='User2', owner=self.user)
        self.book_3 = Book.objects.create(name='The lord of the rings', price=900.00, 
                                          author='User3', owner=self.user)

    def test_ok(self):

        data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        expected_result = [
            {
                "id": self.book_1.id,
                "name": "Harry Potter",
                "price": "1000.00",
                'author': 'User1',
                'owner': self.user.id,
            },
            {
                "id": self.book_2.id,
                "name": "The Witcher",
                "price": "700.00",
                'author': 'User2',
                'owner': self.user.id,
            },
                        {
                "id": self.book_3.id,
                "name": "The lord of the rings",
                "price": "900.00",
                'author': 'User3',
                'owner': self.user.id,
            }
        ]

        self.assertEqual(expected_result, data)


