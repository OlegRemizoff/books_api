from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Avg
from django.db.models import Case, When
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer
import json


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, 
                                          author='J. K. Rowling', owner=self.user)
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00, author='Andrzej Sapkowski')
        self.book_3 = Book.objects.create(name='The lord of the Rowling', price=900.00, author='Tolkien')
        UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True, rate=5)

    def test_get(self):
        # url = reverse('book-list') # смотреть в роутерах URL Name или в шаблоне при запуске сервера
        url = '/book/'  # 'http://127.0.0.1:8000/book/'
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate')
            ).order_by('id')
        # serializer_data  = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        serializer_data  = BooksSerializer(books, many=True).data
        

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        # self.assertEqual(serializer_data[0]['likes_count'], 1)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)


    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Rowling'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate')
        ).order_by('id')

        # serializer_data  = BooksSerializer([self.book_1, self.book_3], many=True).data | old
        serializer_data  = BooksSerializer(books, many=True).data # | new

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)



    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # rating=Avg('userbookrelation__rate')
            ).order_by('price')
        # serializer_data  = BooksSerializer([self.book_2, self.book_3, self.book_1], many=True).data |old
        serializer_data  = BooksSerializer(books, many=True).data # |new

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())

        url = reverse('book-list')
        data = {
            "name": "Страж",
            "price": "259.00",
            "author": "Алексей Пехов"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)


    def test_update(self):       
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": "99.00",
            "author": self.book_1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # пересоздадим книгу т.к она изменилась в DB, но в нашем классе она не меняется
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(99, self.book_1.price)


    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_user2')    
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": "99.00",
            "author": self.book_1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.', code='permission_denied')}, response.data)
        self.book_1.refresh_from_db()
        self.assertEqual(1000, self.book_1.price)

    def test_update_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_user2', is_staff=True) 
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": "103.00",
            "author": self.book_1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # пересоздадим книгу т.к она изменилась в DB, но в нашем классе она не меняется
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(103, self.book_1.price)      


    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url, content_type="application/json")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Book.objects.all().count())


    def test_delete_not_owner(self):
        self.user2 = User.objects.create(username='test_user2')
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, content_type="application/json")
        
        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.', code='permission_denied')}, response.data)
        self.assertEqual(3, Book.objects.all().count())


    def test_delete_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_user2', is_staff=True) 
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, content_type="application/json")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Book.objects.all().count())


class BooksRelationTestCase(APITestCase):
# ./manage.py test store.tests.test_api.BooksRelationTestCase.test_like
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1', is_staff=True)
        self.user2 = User.objects.create(username='test_user2')
        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, 
                                          author='J. K. Rowling', owner=self.user1)
        self.book_2 = Book.objects.create(name='The Witcher', price=700.00, author='Andrzej Sapkowski')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id, ))
        data = {
            "like": True,

        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book_1)


        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,

        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)


    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id, ))
        data = {
            "rate": 3,

        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book_1)


        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, relation.rate)


    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id, ))
        data = {
            "rate": 6,

        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book_1)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
        # AssertionError: 200 != 400 : {'rate': [ErrorDetail(string='Значения 6 нет среди допустимых вариантов.', code='invalid_choice')]}
