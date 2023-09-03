from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.db.models.aggregates import Count
from django.db.models import Case, When
from .models import Book, UserBookRelation
from .serializers import BooksSerializer, UserBookRelationSerializer

class BookViewSet(ModelViewSet):
    queryset =books = Book.objects.all().annotate(
        annotated_likes=Count(
            Case(
                When(
                    userbookrelation__like=True, then=1)
                    )))
        
    serializer_class = BooksSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price', 'author']
    search_fields = ['name', 'price', 'author']
    ordering_fields = ['id', 'name', 'author', 'price']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, 
                                                        book_id = self.kwargs['book'])
        return obj


def home(request):
    return render(request, 'index.html', )


def logut_view(request):
    logout(request)
    return redirect('home')