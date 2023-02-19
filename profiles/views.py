from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, Preference
from .serializers import ProfileSerializer, PreferenceSerializer
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from onlyevents_drf_api.permissions import IsProfileOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List profiles.
    Define and add to the queryset events_count,
    followers_count, and following_count fields.
    -Filter profiles with followers so that
    we can retrieve all profiles that follow a user
    by the user profile id.
    -Filter profiles with followers so that
    we can retrieve all profiles belonging to the users
    followed by a given profile id.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile'
    ]
    orderin_fields = [
        'events_count',
        'followers_count',
        'following_count'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve a profile, or update it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')


class PreferenceList(generics.ListCreateAPIView):
    """
    List preferences or create a preference if logged in.
    -Filter preferences with profiles so that
    we can retrieve all preferences belonging to a user
    by a given profile id.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PreferenceSerializer
    queryset = Preference.objects.all()
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'profile'
    ]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class PreferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a preference, update, or delete it by id if you
    own the profile to which the preference is related.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
