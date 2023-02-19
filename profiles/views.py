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
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')


class PreferenceList(generics.ListCreateAPIView):
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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
