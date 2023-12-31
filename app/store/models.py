from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    def __str__(self) -> str:
        return f'id: {self.id} | {self.name}'
    

class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self) -> str:
        return f'{self.user.username} | {self.book.name} | {self.rate}'
    
    def save(self, *args, **kwargs):
        from store.utils import set_rating

        creating = not self.pk
        old_rating = self.rate 

        super().save(*args, **kwargs) # обращаемся к родительскому классу, что-бы не перезаписать его а вызвать
        new_rating = self.rate
        
        if old_rating != new_rating or creating :
            set_rating(self.book) 

# Залайканные или имеют рейтинг | related_name='books' | user.books.all(): 
# <QuerySet [<Book: id: 5 | Страж>, <Book: id: 1 | Harry Potter and the philosopher']>

# Owner | related_name='my_books' | user.my_books.all():
# <QuerySet [<Book: id: 1 | Harry Potter and the philosopher's stone>, <Book: id: 2 | The Witcher>]>