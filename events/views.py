from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from onlyevents_drf_api.permissions import IsEventOwnerOrReadOnly
from onlyevents_drf_api.permissions import IsGalleryOwnerOrReadOnly
from .models import Event, Gallery, Photo, EventGenre
from .serializers import EventSerializer, GallerySerializer
from .serializers import PhotoSerializer, PhotoDetailSerializer
from .serializers import EventGenreSerializer, EventGenreDetailSerializer


class EventList(generics.ListCreateAPIView):
    """
    List events or create an event if logged in.
    Define and add to the queryset a comments_count,
    interesteds_count, and goings_count fields.
    -Filter events with followers so that
    we can retrieve all events belonging to the users
    followed by a given profile id.
    -Filter events with interested so that
    we can retrieve all events a user is interested
    in by giving their profile id.
    -Filter events with goings so that
    we can retrieve all events a user is going to,
    by giving their profile id.
    -Filter events with a given profile id to
    retrieve all events posted by a specific user.
    -Filter events by category.
    -Filter events by their genre.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        comments_count=Count('comment', distinct=True),
        interesteds_count=Count('interesteds', distinct=True),
        goings_count=Count('goings', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    search_fields = [
        'owner__username',
        'title',
        'date'
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'interesteds__owner__profile',
        'goings__owner__profile',
        'owner__profile',
        'category',
        'event_genres__genre__preference__profile'
    ]
    ordering_fields = [
        'comments_count',
        'interesteds_count',
        'goings_count'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an event, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        comments_count=Count('comment', distinct=True),
        interesteds_count=Count('interesteds', distinct=True),
        goings_count=Count('goings', distinct=True)
    ).order_by('-created_at')


class GalleryList(generics.ListAPIView):
    """
    List galleries.
    """
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()


class GalleryDetail(generics.RetrieveUpdateAPIView):
    """
        Retrieve a gallery, or update it by id if you own it.
    """
    permission_classes = [IsGalleryOwnerOrReadOnly]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()


class PhotoList(generics.ListCreateAPIView):
    """
    List photos or create a photo if logged in.
    -Filter photos with a given profile id to
    retrieve all photos posted by a specific user.
    - Filter photos with the event to retrieve all photos
    of a specific event by a given event id.
     -Filter photos with followers so we can
    retrieve all photos belonging to the users
    followed by a given profile id.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__profile',
        'gallery__posted_event',
        'owner__followed__owner__profile'
    ]

    ordering_fields = [
        'created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve a photo, or update, or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()


class EventGenreList(generics.ListCreateAPIView):
    """
    List event genres or create an event genre if
    owner of the event to which the genre is related, and
    if the genre category and the event category match.
    """
    serializer_class = EventGenreSerializer
    queryset = EventGenre.objects.all()
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'event'
    ]

    def perform_create(self, serializer):
        if (self.request.user != serializer.validated_data['event'].owner):
            raise ValidationError(
                "You cannot add a genre to someone else event")
        serializer.save()


class EventGenreDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve an event genre, or update it by id if
        you own the event to which the genre is related.
    """
    permission_classes = [IsEventOwnerOrReadOnly]
    serializer_class = EventGenreSerializer
    queryset = EventGenre.objects.all()

    def perform_update(self, serializer):
        if (self.request.user != serializer.validated_data['event'].owner):
            raise ValidationError(
                "You cannot add a genre to someone else event")
        serializer.save()
