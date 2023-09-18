from django.test import TestCase
from store.models import User, Book, UserBookRelation
from store.utils import set_rating




class SetRatingTestCase(TestCase):
    # ./manage.py test store.tests.test_utils.SetRatingTestCase
    def setUp(self):
        self.user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Ivanov')
        self.user2 = User.objects.create(username='user2', first_name='Petr', last_name='Petrov')
        self.user3 = User.objects.create(username='user3', first_name='1', last_name='2')

        self.book_1 = Book.objects.create(name='Harry Potter', price=1000.00, 
                                          author=self.user1.username, owner=self.user1)

        # Лайкаем и оцениваем
        UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True, rate=4)


    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))
        
        

