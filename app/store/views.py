from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Book
from .serializers import BooksSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price', 'author']
    search_fields = ['name', 'price', 'author']
    ordering_fields = ['id', 'name', 'author', 'price']


def home(request):
    return render(request, 'index.html', )


def logut_view(request):
    logout(request)
    return redirect('home')