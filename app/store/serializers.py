from rest_framework import serializers
from .models import Book, UserBookRelation


class BooksSerializer(serializers.ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', # User.username стандартный атрибут модели User
                                       default="", read_only=True) 

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author', 'annotated_likes', 'rating', 'owner_name') #' likes_count',

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count() # instance текущая книга
    

class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')