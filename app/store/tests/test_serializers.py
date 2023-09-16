from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Avg
from django.db.models import Case, When
from store.serializers import BooksSerializer
from store.models import Book, UserBookRelation



class BookSerializerTestCase(TestCase):
    # ./manage.py test store.tests.test_serializers.BookSerializerTestCase
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, 
                                          author=self.user1, owner=self.user1)
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00,
                                          author=self.user2, owner=self.user2)
        self.book_3 = Book.objects.create(name='The lord of the rings', price=900.00, 
                                          author=self.user3)

        # Лайкаем и оцениваем
        UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True, rate=4)

        UserBookRelation.objects.create(user=self.user1, book=self.book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user2, book=self.book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=self.user3, book=self.book_2, like=False)

    def test_ok(self):

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
            ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_result = [
            {
                "id": self.book_1.id,
                "name": "Harry Potter",
                "price": "1000.00",
                'author': self.user1.username,     
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user1',
                # 'likes_count': 3,
            },
            {
                "id": self.book_2.id,
                "name": "The Witcher",
                "price": "700.00",
                'author': self.user2.username,
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': 'user2',
                # 'likes_count': 2,
            },
                        {
                "id": self.book_3.id,
                "name": "The lord of the rings",
                "price": "900.00",
                'author': self.user3.username,
                'annotated_likes': 0,
                'rating': None,
                'owner_name': '',
                # 'likes_count': 0,
            }
        ]

        # print(expected_result)
        # print('================')
        # print(data)
        self.assertEqual(expected_result, data)

