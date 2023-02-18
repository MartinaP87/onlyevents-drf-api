from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
