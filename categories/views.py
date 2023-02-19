from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from onlyevents_drf_api.permissions import IsAdminOrReadOnly
from .models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer


class CategoryList(generics.ListCreateAPIView):
    """
    List categories or create a category if superuser.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            return serializer.save()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a category, or update or delete it by id if admin.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreList(generics.ListCreateAPIView):
    """
    List genres or create a genre if superuser.
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            return serializer.save()


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a genre, or update or delete it by id if admin.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
