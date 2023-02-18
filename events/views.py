from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import generics, permissions
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from onlyevents_drf_api.permissions import IsEventOwnerOrReadOnly
from onlyevents_drf_api.permissions import IsGalleryOwnerOrReadOnly
from .models import Event, Gallery, Photo, EventGenre
from .serializers import EventSerializer, GallerySerializer
from .serializers import PhotoSerializer, PhotoDetailSerializer
from .serializers import EventGenreSerializer, EventGenreDetailSerializer


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class GalleryList(generics.ListAPIView):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()


class GalleryDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsGalleryOwnerOrReadOnly]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()


class PhotoList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()


class EventGenreList(generics.ListCreateAPIView):
    serializer_class = EventGenreSerializer
    queryset = EventGenre.objects.all()

    def perform_create(self, serializer):
        if (self.request.user != serializer.validated_data['event'].owner):
            raise ValidationError(
                "You cannot add a genre to someone else event")
        if serializer.validated_data[
         'event'].category != serializer.validated_data['genre'].category:
            raise ValidationError(
                "You can't add a genre of a different event category"
            )
        serializer.save()


class EventGenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEventOwnerOrReadOnly]
    serializer_class = EventGenreDetailSerializer
    queryset = EventGenre.objects.all()
