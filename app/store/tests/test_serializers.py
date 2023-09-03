from django.test import TestCase
from django.contrib.auth.models import User
from store.serializers import BooksSerializer
from store.models import Book, UserBookRelation



class BookSerializerTestCase(TestCase):
    # ./manage.py test store.tests.test_serializers.BookSerializerTestCase
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, 
                                          author=self.user1)
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00,
                                          author=self.user2)
        self.book_3 = Book.objects.create(name='The lord of the rings', price=900.00, 
                                          author=self.user3)

        UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True)
        UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True)

        UserBookRelation.objects.create(user=self.user1, book=self.book_2, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book_2, like=True)
        UserBookRelation.objects.create(user=self.user3, book=self.book_2, like=False)

    def test_ok(self):

        data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        expected_result = [
            {
                "id": self.book_1.id,
                "name": "Harry Potter",
                "price": "1000.00",
                'author': self.user1.username,
                'likes_count': 3,
            },
            {
                "id": self.book_2.id,
                "name": "The Witcher",
                "price": "700.00",
                'author': self.user2.username,
                'likes_count': 2,
            },
                        {
                "id": self.book_3.id,
                "name": "The lord of the rings",
                "price": "900.00",
                'author': self.user3.username,
                'likes_count': 0,
            }
        ]

        print(expected_result)
        print('================')
        print(data)
        self.assertEqual(expected_result, data)


