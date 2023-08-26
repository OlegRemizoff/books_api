from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'id: {self.id} | {self.name}'