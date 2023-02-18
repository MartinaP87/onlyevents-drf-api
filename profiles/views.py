from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import Profile, Preference
from .serializers import ProfileSerializer, PreferenceSerializer
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from onlyevents_drf_api.permissions import IsProfileOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class PreferenceList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PreferenceSerializer
    queryset = Preference.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class PreferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
