from rest_framework import serializers
from .models import Book, UserBookRelation


class BooksSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author', 'likes_count', 'annotated_likes')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count() # instance текущая книга
    

class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')